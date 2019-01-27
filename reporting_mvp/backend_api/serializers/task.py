from . import comment
from master_data.models import tasks
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    comment_set = comment.CommentSerializer(many=True)

    class Meta:
        model = tasks.Task
        fields = ('id', 'name', 'external_id', 'comment_set')
