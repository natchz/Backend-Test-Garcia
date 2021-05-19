from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    created = models.DateTimeField(_("created"), auto_now_add=True, blank=True, editable=False)
    modified = models.DateTimeField(_("modified"), auto_now=True, blank=True, editable=False)

    class Meta:
        get_latest_by = "modified"
        abstract = True