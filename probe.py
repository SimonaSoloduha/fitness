# 7
# from typing import Callable
#
#
# def create_handlers(callback: Callable) -> list:
#     """Функция для добавляем обработчики для каждого шага (от 0 до 4)
#
#     :param callback: объект типа Callable
#     :type callback: Callable
#     :return: handlers_list: список с обработчиками для каждого шага (от 0 до 4)
#     :rtype: list
#     """
#
#     handlers_list = [lambda x=callback, step=step: callback(step) for step in range(5)]
#     return handlers_list
#
#
# def execute_handlers(handlers_list: list) -> None:
#     """Функция для запуска списка с обработчиками (шаги от 0 до 4)
#
#     :param handlers_list: список с обработчиками для каждого шага (от 0 до 4)
#     :type handlers_list: list
#
#     """
#     for handler in handlers_list:
#         handler()


# 8
#
# def remove_duplicates(list_with_duplicates: list) -> list:
#     """Функция для удаления дубликатов из списка словарей
#
#     :param list_with_duplicates: список словарей
#     :type list_with_duplicates: list
#     :return: list_without_duplicates: список словарей без дубликатов
#     :rtype: list
#     """
#
#     list_without_duplicates = [dict(s) for s in set(frozenset(d.items()) for d in list_with_duplicates)]
#     return list_without_duplicates

# 9
#
# import requests
# from bs4 import BeautifulSoup
#
# url = 'https://jetlend.ru/borrower/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
#
#
# def get_count_tags() -> str:
#     """Функция для получения количества HTML-тегов в коде главной страницы сайта jetlend.ru
#
#     :return: Ответ в формате строки
#     :rtype: str
#     """
#     elem_all_count = len(soup.find_all(True))
#     elem_with_attrs_count = len(soup.find_all(attrs=True))
#     return f'Всего HTML-тегов в коде главной страницы сайта jetlend.ru: {elem_all_count}, ' \
#            f'из них содержат атрибуты: {elem_with_attrs_count}.'
#
#
# print(get_count_tags())


# 10
#
#
# def get_queryset(self):
#     queryset = Borrower.objects.all()
#
#     # Число заемщиков, имеющих закрытые займы (status = closed).
#     borrowers_with_loans_status_closed = queryset.filter(loans__status=2).distinct().count()
#
#     # Число заемщиков, для которых существует хотя бы один заем, созданный в 2022 году.
#     borrowers_with_loans_created_at_in_2022 = queryset.filter(loans__created_at__year=2022).distinct().count()
#     # Совокупный объем (amount) всех активных займов (status = active),
#     # принадлежащим заемщикам, которые зарегистрировались в 2021 году.
#     loans_amount = queryset.filter(created_at__year=2021, loans__status=1).aggregate(Sum('loans__amount'))[
#         'loans__amount__sum']
#
#     print('borrowers_with_loans_status_closed', borrowers_with_loans_status_closed,
#           'borrowers_with_loans_created_at_in_2022', borrowers_with_loans_created_at_in_2022,
#           'loans_amount', loans_amount)
#     return queryset


# 11.Напишите функцию на Python, которая возвращает текущий публичный IP-адрес компьютера (например, с использованием сервиса ifconfig.me).


# import http.client
#
# def get_ip():
#     conn = http.client.HTTPConnection("ifconfig.me")
#     conn.request("GET", "/ip")
#     ip = conn.getresponse().read().decode('utf-8')
#     return ip
#
# print(get_ip())

# # 12
# @transaction.atomic
# @api_view(['POST'])
# def api_create_investor(request):
#       investor = Investor.objects.create()
#       investor_task.delay(investor.id)
#       return Response({"status": "OK"})
#
#
# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 5})
# def investor_task(self, investor_id):
#     try:
#         investor = Investor.objects.get(pk=investor_id)
#         investor.processed = True
#         investor.save()
#         time.sleep(0.5) # эмуляция долгой работы метода - сама по себе проблемой не является
#     except Exception:
#         logger.exception(f"Report error here {ex}")
#         pass


# 13


# class Investor(models.Model):
#     ...
#
#     def update_a_100(self, balance):
#         Investor.objects.filter(pk=self.pk).update(a=F('a') + 100)
#
#     def update_b_100(self, balance):
#         Investor.objects.filter(pk=self.pk).update(b=F('b') + 100)
#
#
# @api_view(['POST'])
# @transaction.atomic
# def api_increase_a(request, investor_id):
#     try:
#         investor = Investor.objects.get(pk=investor_id)
#         investor.update_a_100()
#         time.sleep(0.5) # эмуляция долгой работы метода - сама по себе проблемой не является
#         investor.save()
#         return Response({"status": "OK"})
#     except Exception:
#         logger.exception(f"Report error here {ex}")
#         transaction.rollback()
#         return Response({"status": "False"})
#
#
#
# @api_view(['POST'])
# @transaction.atomic
# def api_increase_b(request, investor_id):
#     try:
#         investor = Investor.objects.get(pk=investor_id)
#         investor.update_b_100()
#         time.sleep(0.5) # эмуляция долгой работы метода - сама по себе проблемой не является
#         investor.save()
#         return Response({"status": "OK"})
#     except Exception as ex:
#         logger.exception(f"Report error here {ex}")
#         transaction.rollback()
#         return Response({"status": "False"})


# Думаю может организоваться гонка состояний


# 14
# openpyxl
#
# import os
# import pandas as pd
# from pandas import DataFrame
#
#
# def normalize_path(path: str) -> str:
#     """Функция для нормализации пути к файлу
#
#     :param path: путь к файлу .xlsx
#     :type path: str
#     :return: path - нормализованный путь к файлу .xlsx
#     :rtype: str
#     """
#     path = os.path.abspath(path)
#     return path
#
#
# def get_df_from_file(file_location: str) -> DataFrame:
#     """Функция для получения экземпляр DataFrame из файла .xlsx
#
#     :param file_location: путь к файлу .xlsx
#     :type file_location: str
#     :return: df - экземпляр DataFrame
#     :rtype: DataFrame
#     """
#     df = pd.read_excel(file_location)
#     return df
#
#
# def get_sum_amount_before_2021(df: DataFrame) -> str:
#     """Функция для вчисление cумма всех займов для компаний, зарегистрированных не позднее 2021 года.
#
#     :param df: экземпляр DataFrame
#     :type df: DataFrame
#     :return: sum_amount_before_2021 cумма всех займов для компаний, зарегистрированных не позднее 2021 года
#     :rtype: str
#     """
#
#     sum_amount_before_2021 = df.loc[(df['registration_data'].dt.year < 2021)]['amount'].sum()
#     sum_amount_before_2021 = int(sum_amount_before_2021)
#     return f'Сумма всех займов для компаний, зарегистрированных не позднее 2021 года: {sum_amount_before_2021}'
#
#
# def get_sum_for_rating(df: DataFrame) -> str:
#     """Функция для вычисление сумм займов для каждого из рейтингов.
#
#     :param df: экземпляр DataFrame
#     :type df: DataFrame
#     :return: sum_for_rating результат в виде таблицы с двумя колонками — рейтинг и сумма
#     :rtype: str
#     """
#     sum_for_rating = df.groupby(['rating'])['amount'].sum().reset_index(name='sum')
#     sum_for_rating = sum_for_rating.to_string(index=False)
#     return f'Сумма займов для каждого из рейтингов\n {sum_for_rating}'
#
#
# def get_result():
#     path = input('Введите полный путь к файлу в формате.xlsx (Например /Users/applestock/Desktop/test.xlsx )\n')
#     path = normalize_path(path)
#     df = get_df_from_file(path)
#     print(get_sum_amount_before_2021(df))
#     print(get_sum_for_rating(df))
#
#
# if __name__ == "__main__":
#     get_result()




# def get_combinations(number_n, number_m):
#     """Функция для вчисление всех возмоных комбинаций числа 12345678910111213...N,
#     для получения суммы числа M
#
#     :param number_n: натуральное число N (для поиска комбинаций)
#     :type number_n: int
#     :param number_m: натуральное число M (сумма)
#     :type number_m: int
#     :return: set c вариантами вычисления
#     :rtype: set
#     """
#
#     number_n = list(i for i in range(1, int(number_n) + 1))
#     number_n = int(''.join(map(str, number_n)))
#
#     result_set = []
#     for k in (range(1, number_n)):
#         for i in combinations(range(1, number_n), k):
#             if int(i[0]) <= number_m:
#                 if sum(i) == number_m:
#                     result_set.append(i)
#                 if sum(i) >= number_m:
#                     break
#     return result_set
# docker run hello-world
# docker run -it ubuntu bash
#
# touch .dockerignore

# touch .dockerignore
# echo "db.sqlite" >> .dockerignore
# echo ".venv" >> .dockerignore
# echo "__pycache__" >> .dockerignore
# docker-compose up
# docker-compose build
# docker-compose up -d

