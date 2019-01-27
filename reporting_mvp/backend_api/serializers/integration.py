from django.contrib.auth.models import User
from master_data.models.integrations import Integrations
from rest_framework import serializers


class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integrations
        fields = ('id', 'service_name')
