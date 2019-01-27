from django.contrib.auth.models import User
from master_data.models.projects import Project
from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'external_id', 'integration_id')
