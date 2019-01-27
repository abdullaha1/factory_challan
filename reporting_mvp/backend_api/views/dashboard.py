from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from backend_api.serializers import dashboard
from master_data.models.dashboard import Dashboard


@method_decorator(csrf_exempt, name='dispatch')
class DashboardViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = dashboard.DashboardSerializer
    queryset = Dashboard.objects.filter().all()
