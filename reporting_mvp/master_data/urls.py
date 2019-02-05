from django.contrib import admin
from django.urls import path, include
from master_data import views
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
        views.home.HomeView.as_view(),
        name='home'),
    path(
        'data/',
        views.home.DataView.as_view(),
        name='data')
]
