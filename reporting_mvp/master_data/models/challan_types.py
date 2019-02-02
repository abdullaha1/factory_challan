from django.db import models

from .base_model import Base


class ChallanTypes(Base):
    """
    This Model takes Challan Types
    Available Types: Bill and Delivery
    """
    name = models.TextField()

