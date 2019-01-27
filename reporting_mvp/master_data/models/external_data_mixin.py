from django.db import models


class ExternalDataMixin(models.Model):
    """
    This model will b used as a base model for all classes
    """
    external_id = models.TextField(unique=True)
    integration = models.ForeignKey("Integrations",
                                    on_delete=models.PROTECT,
                                    related_name="%(class)s_integration")
    source_created_at = models.DateTimeField(null=True)
    source_updated_at = models.DateTimeField(null=True)
    source_created_by = models.TextField(null=True)
    source_updated_by = models.TextField(null=True)

    class Meta:
        abstract = True
