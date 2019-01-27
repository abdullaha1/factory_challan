from django.db import models
from django.contrib.auth.models import User

from .base_model import Base
from .external_data_mixin import ExternalDataMixin


class Workspace(Base, ExternalDataMixin):
    """
    This Model takes company details
    """
    name = models.TextField()
    description = models.TextField(null=True)
    users = models.ManyToManyField("auth.User")
    current_status = models.TextField(null=True)

