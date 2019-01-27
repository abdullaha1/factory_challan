from django.contrib import admin
from django.urls import path, include
from master_data.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path(
        '',
        LoginView.as_view(),
        name='login'),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logut'),
    path(
        'home/',
        home.HomeView.as_view(),
        name='home')
]
