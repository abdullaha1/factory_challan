from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt


from backend_api.views import workspace
from backend_api.views import challan
router = routers.DefaultRouter()

router.register(r'challan', challan.ChallanViewSet, base_name='challan')
router.register(r'challan-columns', challan.ChallanColumnViewSet, base_name='challan-columns')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]