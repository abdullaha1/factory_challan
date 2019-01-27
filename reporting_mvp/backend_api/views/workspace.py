from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend_api.serializers import workspace
from master_data.models.workspaces import Workspace


class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = workspace.WorkspaceSerializer

    @action(detail=True, url_path='get-workspace', url_name='get-workspace')
    def get_workspaces(self, request, pk):
        response = {}
        response['task_id'] = self.request.session.get('task_id', '')
        response['workspace'] = Workspace.objects.filter(created_by_id=self.request.user.id).\
            values('id', 'name', 'external_id', 'integration_id')
        return Response(data=response)

    def get_queryset(self):
        return Workspace.objects.filter(
                                    created_by_id=self.request.user.id
        )
