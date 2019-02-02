from rest_framework import viewsets

from backend_api.serializers import challan
from master_data.models.challan_types import ChallanTypes
from master_data.models.challan_columns import ChallanColumns


class ChallanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChallanTypes.objects.filter().all()
    serializer_class = challan.ChallanSerializer


class ChallanColumnViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return ChallanColumns.objects.filter(challan_id=self.request.GET.get('challan_id', '')).select_related('challan_id').all()
    serializer_class = challan.ChallanColumnSerializer
