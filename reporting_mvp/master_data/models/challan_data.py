import datetime


from django.db import models
from django.contrib.postgres.fields import JSONField


from .base_model import Base


class ChallanData(Base):
    """
    This Model takes company details
    """
    challan_type_id = models.ForeignKey(
        'ChallanTypes', on_delete=models.PROTECT
    )
    data = JSONField()
