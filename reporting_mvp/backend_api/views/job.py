from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from backend_api.serializers import jobs
from master_data.models.jobs import Job


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = jobs.JobSerializer

    def get_queryset(self):
        return Job.objects.filter(created_by_id=self.request.user.id, job_id=self.request.GET.get('task_id'))
