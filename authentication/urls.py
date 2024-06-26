from django.urls import path

from authentication.views import (register_user, logout_user, login_user, reset_password_1, reset_password_2,
                                  reset_password_3)

urlpatterns = [
    path('register', register_user, name='register'),
    path('login_fitness', login_user, name='login_fitness'),
    path('logout_fitness', logout_user, name='logout_fitness'),
    path('reset_password_1', reset_password_1, name='reset_password_1'),
    path('reset_password_2', reset_password_2, name='reset_password_2'),
    path('reset_password_3', reset_password_3, name='reset_password_3'),
]
