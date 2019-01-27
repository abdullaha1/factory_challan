from django.contrib.auth.models import User
from master_data.models.dashboard import Dashboard
from rest_framework import serializers


class DashboardSerializer(serializers.ModelSerializer):



    class Meta:
        model = Dashboard
        fields = '__all__'
