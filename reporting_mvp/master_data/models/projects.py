from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField,JSONField

from .base_model import Base
from .external_data_mixin import ExternalDataMixin
from utils.constants import *


class Project(Base, ExternalDataMixin):
    """
    This Model takes company details
    """
    name = models.TextField()
    description = models.TextField(null=True)
    workspace = models.ForeignKey("Workspace", null=True, on_delete=models.PROTECT)
    users = models.ManyToManyField("auth.User")
    current_status = models.TextField(null=True)
    parent_id = models.TextField(null=True)
    labels = JSONField(null=True)
