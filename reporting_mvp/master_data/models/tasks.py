from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField,JSONField


from .base_model import Base
from .external_data_mixin import ExternalDataMixin


class Task(Base, ExternalDataMixin):
    """
    This Model takes company details
    """
    name = models.TextField()
    description = models.TextField(null=True)
    users = models.ManyToManyField("auth.User")
    project = models.ForeignKey("Project", on_delete=models.PROTECT)
    completed_on = models.TextField(null=True)
    reporter_id = models.TextField(null=True)
    current_status = models.TextField(null=True)
    assignee_id = models.TextField(null=True)
    priority = models.TextField(null=True)
    estimate = models.TextField(null=True)
    estimate_unit = models.TextField(null=True)
    media_count = models.TextField(null=True)
    parent_id = models.TextField(null=True)
    labels = JSONField(null=True)
