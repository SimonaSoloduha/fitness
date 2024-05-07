# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect

from authentication.forms import RegisterForm, ResetPassword1, CodeForm, CustomSetPasswordForm
from authentication.tasks import send_code_to_email
from django.utils.translation import gettext_lazy as _


def register_user(request):
    """
    Представление регистрации
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=user.username, email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_user(request):
    """
    Представление авторизации
    """

    context = {
        'form': AuthenticationForm(),
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            login(request, user)
            return redirect('index')
        else:
            try:
                if '@' in username:
                    User.objects.get(email=username)
                else:
                    User.objects.get(username=username)
                attention = _('Неверно указан пароль')
            except User.DoesNotExist:
                attention = _('Пользователя с таким логином или почтой нет.\n'
                               'Проверьте правильно ли указан email или зарегестрируйтесь')
            context = {
                'form': AuthenticationForm(),
                'attention': attention,
            }

    return render(request, 'authentication/login.html', context)


class Logout(LogoutView):
    print('tuuutt')
    """
    Представление выхода
    """
    next_page = 'index'


def logout_user(request):
    logout(request)
    context = {
        'form': AuthenticationForm(),
    }
    return render(request, 'authentication/login.html', context)


def reset_password_1(request):
    """
    Представление восстановления пароля, шаг 1 - введение email
    """
    if request.method == "POST":
        form = ResetPassword1(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                request.session['pk'] = user.pk
                return redirect('reset_password_2')
            except User.DoesNotExist:
                context = {
                    'form': ResetPassword1(),
                    'attention': _('Пользователя с такой почтой нет.\n'
                                   'Проверьте правильно ли указан email или зарегестрируйтесь.')
                }

    else:
        context = {
            'form': ResetPassword1(),
        }
    return render(request, 'authentication/reset_password_1.html', context)


def reset_password_2(request):
    """
    Представление восстановления пароля, шаг 1 - введение кода, отправленного на email
    """
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    context = {
        'form': form,
    }
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        email = user.email
        if not request.POST:
            send_code_to_email(code, email)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                return redirect('reset_password_3')
            else:
                context = {
                    'form': CodeForm(),
                    'attention': _('Неверный код.')
                }
    return render(request, 'authentication/reset_password_2.html', context)


def reset_password_3(request):
    """
    Создание нового пароля
    """
    pk = request.session.get('pk')
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        form = CustomSetPasswordForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            password1 = form.cleaned_data.get("new_password1")
            password2 = form.cleaned_data.get("new_password2")
            if password1 and password2:
                if password1 != password2:
                    context = {
                        'form': CustomSetPasswordForm(),
                        'attention': _('Пароли не совпадают')
                    }
                else:
                    user.set_password(password2)
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('index')

    else:
        context = {
            'form': CustomSetPasswordForm(),
        }
    return render(request, 'authentication/reset_password_3.html', context)
