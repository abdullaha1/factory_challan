from django.db import models
from .base_model import Base


class Integrations(Base):
    """
    This model will be used to store all service name
    such as asana, jira .
    """
    service_name = models.TextField()
    api_url = models.TextField()
