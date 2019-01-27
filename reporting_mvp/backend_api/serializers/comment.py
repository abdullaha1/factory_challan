from django.contrib.auth.models import User
from master_data.models.comments import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['text']
