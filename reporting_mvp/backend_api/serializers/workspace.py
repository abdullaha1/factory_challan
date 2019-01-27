from django.contrib.auth.models import User
from master_data.models.workspaces import Workspace
from rest_framework import serializers


class WorkspaceSerializer(serializers.ModelSerializer):
    task_id = serializers.SerializerMethodField()

    def get_task_id(self, obj):
        return self.context['request'].session.get('task_id')

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'external_id', 'integration_id', 'task_id')
