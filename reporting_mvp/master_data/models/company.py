from django.db import models

from .base_model import Base
from utils.constants import *


class Company(Base):
    """
    This Model takes company details
    """
    name = models.TextField()
    company_url = models.TextField(null=True)
    active = models.BooleanField(default=True)
    status = models.TextField(choices=STATUS_TYPES, null=True)
