from django.shortcuts import render
from django.views import View
from django.http import *

from master_data.tasks.api_interaction import get_projects
from master_data.tasks.api_interaction import get_project_data


class ProjectListView(View):

    def get(self, request):
        """
        This is the Home Method.
        Redirections from Home come here,
        and home template is rendered with all integrations.
        """
        if request.user.is_authenticated:
            return render(
                request, 'projects.html',
                {
                    "task_id": task.message_id
                })
        else:
            return HttpResponseRedirect("/")


class ProjectDetailView(View):

    def get(self, request):
        """
        This is the Home Method.
        Redirections from Home come here,
        and home template is rendered with all integrations.
        """
        if request.user.is_authenticated:
            task_data = get_project_data.send(request.user.id, args=(request.GET['project_id'], request.user.id, request.GET['integration_id']))
            return render(
                request, 'project_data.html',
                {
                    "task_id": task_data.message_id
                })
        else:
            return HttpResponseRedirect("/")


