from django.db import models

from .base_model import Base


class UserIntegrations(Base):
    """
    This model will be used to store user's integrations
    """
    integrations = models.ForeignKey("Integrations", on_delete=models.PROTECT)
    company = models.ForeignKey('Company', on_delete=models.PROTECT)
