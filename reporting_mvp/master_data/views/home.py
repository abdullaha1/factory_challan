
import dramatiq
from django.shortcuts import render, redirect, render_to_response
from django.views import View
from django.http import *
from master_data.models.workspaces import Workspace

class HomeView(View):

    def get(self, request):
        """
        This is the Home Method.
        Redirections from Home come here,
        and home template is rendered with all integrations.
        """
        if request.user.is_authenticated:

            return render(
                request, 'home.html')
        else:
            return HttpResponseRedirect("/")




class DataView(View):

    def get(self, request):
        """
        This is the Home Method.
        Redirections from Home come here,
        and home template is rendered with all integrations.
        """
        if request.user.is_authenticated:

            return render(
                request, 'data.html')
        else:
            return HttpResponseRedirect("/")