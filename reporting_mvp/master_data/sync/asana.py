"""Sync job for Asana.
"""

from master_data.sync.base import Base
from django.contrib.auth.models import User
from master_data.models.workspaces import Workspace
from master_data.models.integrations_table_mappings import IntegrationsTableMapping
from master_data.models.integrations_column_mappings import IntegrationsColumnMapping
from master_data.models.integrations import Integrations
from master_data.models.projects import Project
from master_data.models.tasks import Task
from master_data.models.comments import Comment
from auth_backends.atlassian import AtlassianOAuth2

import asana


class Asana(Base):

    """
    Initialized Asana Client
    """
    def __init__(self, access_token, user):
        self.client = asana.Client.access_token(access_token)
        self.user = user
    """
    This is the interaction class for Asana API
    """

    def extract_workspaces(self):
        """
        This method fetches workspaces from Asana API, and saves them to database. 
        """
        current_user = self.client.users.me()
        integration = Integrations.objects.get(service_name='asana')
        table = IntegrationsTableMapping.objects.get(destination_table='Workspaces', integrations_id=integration.id)
        columns = IntegrationsColumnMapping.objects.filter(integrations_id=table.id).all()
        for all_workspace in current_user['workspaces']:
            workspace = Workspace.objects.update_or_create(external_id=all_workspace['id'],
                defaults= {
                "created_by": self.user,
                "updated_by": self.user,
                 "integration": integration,
                }
                )[0]
            workspace_details = self.client.workspaces.find_by_id(workspace=all_workspace['id'])
            for column in columns:
                if column.source_column:
                    setattr(workspace, column.destination_column, workspace_details[column.source_column])
            workspace.save()

    def extract_projects(self, workspace_id):
        """
        This method fetches projects from Asana API, and saves them to database. 
        """
        workspace = Workspace.objects.get(id=workspace_id)
        integration = Integrations.objects.get(service_name='asana')
        table = IntegrationsTableMapping.objects.get(destination_table='Projects', integrations_id=integration.id)
        columns = IntegrationsColumnMapping.objects.filter(integrations_id=table.id).all()
        
        for project in self.client.projects.find_by_workspace(workspace=workspace.external_id):
            project_details = self.client.projects.find_by_id(project=project['id'])
            project = Project.objects.update_or_create(external_id=project['id'],
                defaults = {
                "created_by": self.user,
                "updated_by": self.user,
                "integration": integration,
                "workspace": workspace,
                }
                )[0]
            for column in columns:
                if column.source_column:
                    split_column = column.source_column.split('.') 
                    if column.source_column != "workspace.id":
                        if (len(split_column) == 1):
                            setattr(project, column.destination_column, project_details[column.source_column])
                        else:
                            setattr(project, column.destination_column, project_details[split_column[0]][split_column[1]])
            project.save()

    def extract_project_data(self, project_id):
        """
        This method fetches Asana Tasks and Comments inside a Project, and saves them to database.
        """

        project = Project.objects.get(id=project_id)
        integration = Integrations.objects.get(service_name='asana')
        table = IntegrationsTableMapping.objects.get(destination_table='Tasks', integrations_id=integration.id)
        columns = IntegrationsColumnMapping.objects.filter(integrations_id=table.id).all()
        table_comment = IntegrationsTableMapping.objects.get(destination_table='comments', integrations_id=integration.id)
        columns_comment = IntegrationsColumnMapping.objects.filter(integrations_id=table_comment.id).all() 
        status_dict = {}
            
        if project.current_status == "board":
            for section in self.client.sections.find_by_project(project=project.external_id):
                tasks_in_section = self.client.tasks.find_by_section(section=section['id'])
                for task_in_section in tasks_in_section:
                    status_dict[task_in_section['id']] = section['name']

        for task in self.client.tasks.find_by_project(project_id=project.external_id):
            task_details = self.client.tasks.find_by_id(task=task['id'])
            if task['id'] not in status_dict:
                status_dict[task['id']] = None
            task = Task.objects.update_or_create(external_id=task['id'],
                defaults = {
                "created_by": self.user,
                "updated_by": self.user,
                "integration": integration,
                "project": project,
                "labels": "",
                "current_status": status_dict[task['id']]
                })[0]
            for column in columns:
                if column.source_column:
                    split_column = column.source_column.split('.')
                    if column.source_column != "[Project['id']]":
                        if (len(split_column) == 1):
                            setattr(task, column.destination_column, task_details[column.source_column])
                        else:
                            if task_details[split_column[0]]:
                                setattr(task, column.destination_column, task_details[split_column[0]][split_column[1]])
            task.save()
            for story in self.client.stories.find_by_task(task=task.external_id):
                comment = Comment.objects.update_or_create(external_id=story['id'],
                    defaults = {
                    "created_by": self.user,
                    "updated_by": self.user,
                    "integration": integration,
                    "task" : task
                    })[0]
                for column in columns_comment:
                    if column.source_column:
                        split_column = column.source_column.split('.')
                        if column.source_column != "task_id":
                            if (len(split_column) == 1):
                                setattr(comment,column.destination_column,story[column.source_column])
                            elif story[split_column[0]]:
                                setattr(comment,column.destination_column, story[split_column[0]][split_column[1]])
                comment.save()



