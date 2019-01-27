"""Contains the ORM class for tasks.
"""

from django.db import models
from django.contrib.postgres import fields

from .base_model import Base
from utils import constants


class Job(Base):
    """The ORM class for tasks.
    """
    job_id = models.UUIDField()
    type = models.TextField()
    status = models.TextField(choices=constants.JOB_STATUS_TYPES)
    data = fields.JSONField(default=dict)
