from django.contrib.auth.models import User
from master_data.models.challan_types import ChallanTypes
from master_data.models.challan_columns import ChallanColumns
from rest_framework import serializers


class ChallanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallanTypes
        fields = ('id', 'name')


class ChallanColumnSerializer(serializers.ModelSerializer):

    challan_id = ChallanSerializer()

    class Meta:
        model = ChallanColumns
        fields = ('id', 'column', 'type', 'challan_id')
