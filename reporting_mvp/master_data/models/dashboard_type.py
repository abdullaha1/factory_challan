from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField,JSONField

from .base_model import Base
from .external_data_mixin import ExternalDataMixin
from utils.constants import *


class DashboardType(Base):
    """
    This Model takes company details
    """
    name = models.TextField()
    description = models.TextField(null=True)
