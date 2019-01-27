from django.db import models


class UserProfile(models.Model):
    """
    This model will used to store users information
    """
    external_id = models.TextField()
    user = models.OneToOneField("auth.User", on_delete=models.PROTECT)
    token = models.TextField(null=True)
    middle_name = models.TextField(null=True)
