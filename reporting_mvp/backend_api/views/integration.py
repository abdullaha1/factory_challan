from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from backend_api.serializers import integration
from master_data.models.integrations import Integrations


class IntegrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = integration.IntegrationSerializer

    def get_queryset(self):
        return Integrations.objects.filter().all()
