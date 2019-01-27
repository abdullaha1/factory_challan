import dramatiq

from django.contrib.auth.models import User

from master_data.sync import *
from master_data.models.integrations import Integrations
from master_data.models.user_integrations import UserIntegrations
from .base import BaseActor


class FetchWorkspaces(BaseActor):
    actor_name = 'workspaces'

    def perform(self, integration_id, user_id, access_token, external_id, *args, **kwargs):
        """
        This method saves the User, and imports workspaces through Dramatiq background task.
        """
        integration_data = Integrations.objects.get(id=integration_id)
        service_object = INTEGRATION_MAPPER[integration_data.service_name]
        user = User.objects.get(id=user_id)
        user.userprofile.token = access_token
        user.userprofile.external_id = external_id
        user.userprofile.save()
        user.save()
        user_integration = UserIntegrations.objects.update_or_create(company_id=user.userprofile.company_id, defaults={
                'company': user.userprofile.company,
                'integrations': integration_data,
                'created_by': user,
                'updated_by': user,
        })
        service = service_object(access_token, user)
        service.extract_workspaces()


class FetchProjects(BaseActor):

    actor_name = 'projects'

    def perform(self, workspace_id, user_id, integration_id, *args, **kwargs):
        """
            This method imports Projects through Dramatiq background task.
            """
        user = User.objects.get(id=user_id)
        integration_data = Integrations.objects.get(id=integration_id)
        service_object = INTEGRATION_MAPPER[integration_data.service_name]
        service = service_object(user.userprofile.token, user)
        service.extract_projects(workspace_id)


class FetchProjectData(BaseActor):

    actor_name = 'project_data'

    def perform(self, project_id, user_id, integration_id, *args, **kwargs):
        """
            This method imports Tasks and Comments through Dramatiq background task.
            """
        user = User.objects.get(id=user_id)
        integration_data = Integrations.objects.get(id=integration_id)
        service_object = INTEGRATION_MAPPER[integration_data.service_name]
        service = service_object(user.userprofile.token, user)
        service.extract_project_data(project_id)


poll_service = FetchWorkspaces(queue_name='workspaces')
get_projects = FetchProjects(queue_name='projects')
get_project_data = FetchProjectData(queue_name='comments')


