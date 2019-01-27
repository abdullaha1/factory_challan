"""Sync job for Jira.
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

class Jira(Base):
    """
    Initialized Jira Client
    """
    def __init__(self, access_token, user):
        self.client = AtlassianOAuth2()
        self.client.set_access_token(access_token)
        self.user = user

    def extract_workspaces(self):
        """
        This method fetches workspaces from Jira API, and saves them to database. 
        """
        projects = self.client.get_projects()
        integration = Integrations.objects.get(service_name='jira')
        table = IntegrationsTableMapping.objects.get(destination_table='Projects', integrations_id=integration.id)
        columns = IntegrationsColumnMapping.objects.filter(integrations_id=table.id).all()
        for project_details in projects:
            project = Project.objects.update_or_create(external_id=project_details['id'],
                defaults= {
                "created_by": self.user,
                "updated_by": self.user,
                 "integration": integration,
                }
                )[0]
            self.create_record(columns, [], project_details, project)

    def extract_project_data(self,project_id):
        """
        This method fetches Jira Tasks(Issues) and Comments inside a Project, and saves them to database.
        """
        project = Project.objects.get(id=project_id)
        integration = Integrations.objects.get(service_name='jira')
        table = IntegrationsTableMapping.objects.get(destination_table='Tasks', integrations_id=integration.id)
        columns = IntegrationsColumnMapping.objects.filter(integrations_id=table.id).all()
        table_comment = IntegrationsTableMapping.objects.get(destination_table='Comments', integrations_id=integration.id)
        columns_comment = IntegrationsColumnMapping.objects.filter(integrations_id=table_comment.id).all()
        tasks = self.client.get_issues(project.external_id)['issues']
        for task_details in tasks:
            task = Task.objects.update_or_create(external_id=task_details['id'],
                defaults = {
                "created_by": self.user,
                "updated_by": self.user,
                "integration": integration,
                "project": project,
                })[0]
            self.create_record(columns, ["project_id","test"], task_details, task)
            
            comments = self.client.get_comments(task_details['id'])["comments"]
            for comment_details in comments:
                comment = Comment.objects.update_or_create(external_id=comment_details['id'],
                    defaults = {
                    "created_by": self.user,
                    "updated_by": self.user,
                    "integration": integration,
                    "task" : task
                    })[0]
                self.create_record(columns_comment, [], task_details, task)

    def create_record(self, columns, ignore_columns, api_record, record):
        """
        This method uses Column mappings to save a record from API response to DB.
        """
        for column in columns:
            if column.destination_column not in ignore_columns and column.source_column:
                split_column = column.source_column.split('.')
                temp = api_record
                found = True
                for i in split_column:
                    if temp and i in temp:
                        temp = temp[i]
                    else:
                        found = False
                        break
                if found:
                    setattr(record, column.destination_column, temp)
            record.save()