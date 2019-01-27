from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt


from backend_api.views import workspace
router = routers.DefaultRouter()

router.register(r'workspace', workspace.WorkspaceViewSet, base_name='workspace')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]