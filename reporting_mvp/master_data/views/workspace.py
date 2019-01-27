from django.shortcuts import render
from django.views import View
from django.http import *

from master_data.models.workspaces import Workspace


class WorkspaceListView(View):

    def get(self, request):
        """
        This is the Home Method.
        Redirection from Home come here,
        and home template is rendered with all workspaces.
        """
        task_id = request.session.get('task_id')
        if request.user.is_authenticated:
            return render(
                request, 'workspaces.html',
                {
                    "task_id": task_id
                })
        else:
            return HttpResponseRedirect("/")
