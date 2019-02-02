from django.db import models

from .base_model import Base


class ChallanColumns(Base):
    """
    This Model takes Challan Types
    Available Types: Bill and Delivery
    """
    column = models.TextField()
    type = models.TextField()
    challan_id = models.ForeignKey(
        'ChallanTypes', on_delete=models.PROTECT
    )

