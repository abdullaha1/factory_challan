import json
import asana
import dramatiq

from master_data.sync.asana import Asana
from master_data.tasks.api_interaction import poll_service
from master_data.models.integrations import Integrations


def redirection_callback(backend, user, response, strategy, **kwargs):
    """
    Pipeline redirects here with the user and backend info.
    """
    integration_id = strategy.session_get('integration_id')
    integration_object = Integrations.objects.get(id=integration_id)
    if integration_object:
        task = BACKEND_MAPPER[type(backend).__name__](backend, user.id, response, integration_id)
        strategy.session_set('task_id', task.message_id)

def backend_asana_callback (backend, user_id, response, integration_id):
    """
    Polling Asana Service
    """
    return poll_service.send(user_id, args=(integration_id, user_id, response['access_token'], response['data']['id']))


def backend_jira_callback (backend, user_id, response, integration_id):
    """
    Polling Jira Service
    """
    return poll_service.send(user_id, args=(integration_id, user_id, response['access_token'], response['accountId']))


BACKEND_MAPPER = {
    "AsanaOAuth2": backend_asana_callback,
    "AtlassianOAuth2": backend_jira_callback,
}