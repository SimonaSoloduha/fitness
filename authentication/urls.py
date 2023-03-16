from django.urls import path

from authentication.views import register_user, Logout, login_user, reset_password_1, reset_password_2, reset_password_3

urlpatterns = [
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('reset_password_1', reset_password_1, name='reset_password_1'),
    path('reset_password_2', reset_password_2, name='reset_password_2'),
    path('reset_password_3', reset_password_3, name='reset_password_3'),
]
