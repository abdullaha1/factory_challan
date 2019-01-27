from django.contrib.auth.models import User
from master_data.models.jobs import Job
from rest_framework import serializers


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('job_id', 'status', 'type', 'created_on')
