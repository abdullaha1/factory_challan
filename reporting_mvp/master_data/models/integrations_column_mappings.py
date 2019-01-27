from django.db import models

from .base_model import Base


class IntegrationsColumnMapping(Base):
    """
    This model will be use store service table attribute  to our data model
    for jira table tasks
    source_column = description    destination_column = description['content']

    """
    integrations = models.ForeignKey(
        "IntegrationsTableMapping",
        on_delete=models.PROTECT)
    source_column = models.TextField(null=True)
    destination_column = models.TextField(null=True)
