import datetime

from master_data.models.user_profile import UserProfile
from master_data.models.company import Company
from master_data.forms. register import UserProfileRegistrationForm
from master_data.controllers.register import RegisterController

from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.http import *
from django.contrib.auth.models import User
from django.views import View


class RegisterView(View):

    def get(self, request):
        """
         display user registration form
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home')
        upf = UserProfileRegistrationForm()
        return render(request, 'registration/register.html', {'form': upf})

    def post(self, request):
        """Creation of User Profile """
        upf = UserProfileRegistrationForm(request.POST)
        if upf.is_valid():
            user = authenticate(
                request,
                username=request.POST['email'],
                password=request.POST['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/home')
        else:
            return render(request, 'registration/register.html', {
                'form': upf,
            }, status=400)
