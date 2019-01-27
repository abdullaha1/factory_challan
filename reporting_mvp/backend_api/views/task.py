from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from django.db.models import F,Count

from backend_api.serializers import task
from master_data.models.tasks import Task
from master_data.models.comments import Comment


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = task.TaskSerializer

    def get_queryset(self):
        request = self.request
        queryset = Task.objects.filter(integration_id=request.GET['integration_id'], project_id=request.GET['project_id']).prefetch_related(
            Prefetch(
            'comment_set',
            queryset=Comment.objects.filter(integration_id=request.GET['integration_id'])
            )
        )
        return queryset


class TaskChartOnTimeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = task.TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
                created_by_id=self.request.user.id,
                integration_id=self.request.GET['integration_id'],
                project_id=self.request.GET['project_id']
            ).filter(estimate__gt=datetime.now()).\
                values('current_status')\
                .annotate(count=Count('current_status'))

    @action(detail=True, methods=['GET'],  url_path='on-time')
    def on_time(self, request, pk):
        tasks = Task.objects.filter(
            created_by_id=request.user.id,
            integration_id=request.GET['integration_id'],
            project_id=request.GET['project_id'],
            current_status__isnull=False
        ).filter(estimate__gt=datetime.now()).\
            values('current_status')\
            .annotate(count=Count('current_status'))
        return Response(tasks)

    @action(detail=True, methods=['GET'], url_path='late')
    def late(self, request, pk):
        tasks = Task.objects.filter(
            created_by_id=request.user.id,
            integration_id=request.GET['integration_id'],
            project_id=request.GET['project_id'],
            current_status__isnull=False
        ).filter(estimate__lt=datetime.now()). \
            values('current_status') \
            .annotate(count=Count('current_status'))
        return Response(tasks)