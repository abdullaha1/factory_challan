from master_data.models import tasks
from rest_framework import serializers


class TaskChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = tasks.Task
        fields = ('id', 'completed_on', 'estimate')
