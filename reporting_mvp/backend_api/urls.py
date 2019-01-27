from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt


from backend_api.views import job
from backend_api.views import project
from backend_api.views import workspace
from backend_api.views import task
from backend_api.views import task_chart
from backend_api.views import integration
from backend_api.views import dashboard
router = routers.DefaultRouter()

router.register(r'job_status', job.JobViewSet, base_name='job_status')
router.register(r'projects', project.ProjectViewSet, base_name='project')
router.register(r'workspace', workspace.WorkspaceViewSet, base_name='workspace')
router.register(r'task', task.TaskViewSet, base_name='task')
router.register(r'chart', task_chart.TaskViewSet, base_name='chart')
router.register(r'list_integrations', integration.IntegrationViewSet, base_name='integration')
router.register(r'dashboard', dashboard.DashboardViewSet, base_name='dashboard')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]