from django.db import models

from .base_model import Base


class IntegrationsTableMapping(Base):
    """
    this model will be use store service table  to our data model
    for jira
    source_table = issue    destination_table = Tasks
    """
    integrations = models.ForeignKey("Integrations", on_delete=models.PROTECT)
    source_table = models.TextField(null=True)
    destination_table = models.TextField(null=True)
