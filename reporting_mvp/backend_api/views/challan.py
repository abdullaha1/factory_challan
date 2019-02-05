from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from backend_api.serializers import challan
from master_data.models.challan_types import ChallanTypes
from master_data.models.challan_columns import ChallanColumns
from master_data.models.challan_data import ChallanData


class ChallanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChallanTypes.objects.filter().all()
    serializer_class = challan.ChallanSerializer


class ChallanColumnViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return ChallanColumns.objects.filter(challan_id=self.request.GET.get('challan_id', 0)).select_related('challan_id').all()
    serializer_class = challan.ChallanColumnSerializer


class ChallanDataViewSet(viewsets.ModelViewSet):

    queryset = ChallanData.objects.filter().all()
    serializer_class = challan.ChallanDataSerializer


class ChallanDataReadableViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        challan_id = self.request.GET['challan_id']
        fields = ChallanColumns.objects.filter(challan_id=challan_id).values('column')
        dataArray = []
        for field in fields:
            dataArray.append("data__"+field['column'])
        dataArray.append("id")
        return ChallanData.objects.filter(challan_type_id=challan_id).values(*dataArray)

    serializer_class = challan.ChallanDataReadableSerializer
