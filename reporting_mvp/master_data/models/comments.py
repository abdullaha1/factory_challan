from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField,JSONField

from .base_model import Base
from .external_data_mixin import ExternalDataMixin
from utils.constants import *


class Comment(Base, ExternalDataMixin):
    """
    This Model takes company details
    """
    text = models.TextField()
    description = models.TextField(null=True)
    integration = models.ForeignKey("Integrations", on_delete=models.PROTECT)
    task = models.ForeignKey("Task", null=True, on_delete=models.PROTECT)
    project = models.ForeignKey("Project", null=True, on_delete=models.PROTECT)
    users = models.ManyToManyField("auth.User",null=True)
    media_count = models.TextField(null=True)
