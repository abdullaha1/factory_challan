from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt


from backend_api.views import workspace
from backend_api.views import challan
router = routers.DefaultRouter()

router.register(r'challan', challan.ChallanViewSet, base_name='challan')
router.register(r'challan-columns', challan.ChallanColumnViewSet, base_name='challan-columns')
router.register(r'challan-data', challan.ChallanDataViewSet, base_name='challan-data')
router.register(r'challan-data-latest', challan.ChallanLatestViewSet, base_name='challan-data-latest')
router.register(r'challan-data-read', challan.ChallanDataReadableViewSet, base_name='challan-data-read')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]