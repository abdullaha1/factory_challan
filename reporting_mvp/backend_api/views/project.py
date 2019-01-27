from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from backend_api.serializers import project
from master_data.models.projects import Project
from master_data.tasks.api_interaction import get_projects , get_project_data


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = project.ProjectSerializer

    @action(detail=True, url_name='sink-projects', url_path='sink-projects')
    def sink_projects(self, request, pk):
        task = get_projects.send(self.request.user.id, args=(
            request.GET['workspace_id'],
            self.request.user.id,
            request.GET['integration_id']
        ))
        return Response(task.message_id)

    @action(detail=True, url_name='sink-project-data-', url_path='sink-project-data')
    def sink_project_data(self, request, pk):

        task = get_project_data.send(self.request.user.id, args=(
            request.GET['project_id'],
            self.request.user.id,
            request.GET['integration_id']
        ))
        return Response(task.message_id)

    def get_queryset(self):
        return Project.objects.filter(
                    created_by_id=self.request.user.id
        )
