import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action,list_route
from datetime import datetime, timedelta
from django.db.models import Count

from backend_api.serializers import task_chart
from master_data.models.tasks import Task


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = task_chart.TaskChartSerializer

    @action(detail=True, name='task-status',url_path='task-status')
    def task_status(self, request, pk):
        kwargs = {
            'created_by_id':request.user.id,
            'integration_id':request.GET['integration_id'],
            'project_id':request.GET['project_id'],
            }
        filter_data = request.GET['filter_duration'].split(' ')
        if len(filter_data) > 1:
            kwargs['source_updated_at__range'] = (datetime.strptime(filter_data[0], '%Y-%m-%d'),datetime.strptime(filter_data[1], '%Y-%m-%d'))
        else:
            filter_duration = datetime.today() - timedelta(days=int(request.GET['filter_duration']))
            kwargs['source_updated_at__gt'] = filter_duration

        
        tasks = Task.objects.filter(**kwargs)
        data = {
        'early_finish': 0,
        'on_time':0,
        'late':0
        }
        
        for task in tasks:
            if task.estimate:
                if task.completed_on:
                    if (datetime.strptime(task.completed_on,'%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(task.estimate,'%Y-%m-%d')).days == 0:
                        data["on_time"] = data["on_time"] + 1
                    elif datetime.strptime(task.completed_on,'%Y-%m-%dT%H:%M:%S.%fZ') < datetime.strptime(task.estimate,'%Y-%m-%d'):
                        data["early_finish"] = data['early_finish'] + 1
                    else:
                        data["late"] = data["late"] + 1
                elif datetime.strptime(task.estimate,'%Y-%m-%d') < datetime.now():
                    data["late"] = data['late'] + 1

        return Response(json.dumps(data))

    @action(detail=True, methods=['GET'], url_path='on-time')
    def on_time(self, request, pk):
        kwargs = {

            'created_by_id':request.user.id,
            'integration_id':request.GET['integration_id'],
            'project_id':request.GET['project_id'],
            'current_status__isnull':False,
            'estimate__gt':datetime.now(),
        }
        filter_data = request.GET['filter_duration'].split(' ')
        if len(filter_data) > 1:
            kwargs['source_updated_at__range'] = (datetime.strptime(filter_data[0], '%Y-%m-%d'),datetime.strptime(filter_data[1], '%Y-%m-%d'))
        else:
            filter_duration = datetime.today() - timedelta(days=int(request.GET['filter_duration']))
            kwargs['source_updated_at__gt'] = filter_duration

        
        tasks = Task.objects.filter(**kwargs).values('current_status') \
            .annotate(count=Count('current_status'))
        return Response(tasks)

    @action(detail=True, methods=['GET'], url_path='late')
    def late(self, request, pk):

        kwargs = {

            'created_by_id': request.user.id,
            'integration_id': request.GET['integration_id'],
            'project_id': request.GET['project_id'],
            'current_status__isnull':False,
            'estimate__lt': datetime.now(),
        }
        filter_data = request.GET['filter_duration'].split(' ')
        if len(filter_data) > 1:
            kwargs['source_updated_at__range'] = (datetime.strptime(filter_data[0], '%Y-%m-%d'),datetime.strptime(filter_data[1], '%Y-%m-%d'))
        else:
            filter_duration = datetime.today() - timedelta(days=int(request.GET['filter_duration']))
            kwargs['source_updated_at__gt'] = filter_duration

        
        tasks = Task.objects.filter(**kwargs).values('current_status') \
            .annotate(count=Count('current_status'))
        return Response(tasks)




    def get_queryset(self):
        tasks = Task.objects.filter(
            created_by_id=self.request.user.id,
            integration_id=self.request.GET['integration_id'], 
            project_id=self.request.GET['project_id']
            )

        return tasks

