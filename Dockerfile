# Используем базовый образ Python
FROM python:3.8

# Установка переменной окружения для отключения режима буферизации вывода Python
ENV PYTHONUNBUFFERED 1

# Создание и установка рабочей директории /app
WORKDIR /app

# Копирование зависимостей и установка их
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Копирование всего содержимого проекта в рабочую директорию контейнера
COPY . /app/

# Запуск сервера Django при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]