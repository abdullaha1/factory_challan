from django.contrib import admin
from django.urls import path, include
from master_data.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path(
        'register/',
        register.RegisterView.as_view(),
        name='register'),
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
        name='home'),
    path(
        'workspaces/',
        workspace.WorkspaceListView.as_view(),
        name='workspaces'),
    path(
        'projects/',
        project.ProjectListView.as_view(),
        name='projects'),
    path(
        'project/',
        project.ProjectDetailView.as_view(),
        name='project'),
    path(
        'charts/',
        charts.ChartView.as_view())
]
