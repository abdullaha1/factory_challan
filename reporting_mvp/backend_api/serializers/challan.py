from master_data.models.challan_types import ChallanTypes
from master_data.models.challan_columns import ChallanColumns
from master_data.models.challan_data import ChallanData
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


class ChallanDataSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return ChallanData.objects.create(**validated_data)

    class Meta:
        model = ChallanData
        fields = ('id', 'data', 'challan_type_id','created_on')


class ChallanDataReadableSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = ChallanData
        fields = ['data']

    def get_data(self, obj):
        return obj
