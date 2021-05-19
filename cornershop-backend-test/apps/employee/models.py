from django.db import models
from django.urls import reverse
from backend_test.choices import ENABLED_COUNTRIES
from backend_test.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

# Inherit from this class to implement creation and modification track
class Employee(TimeStampedModel):
    """
    Stores employee information including geographic reference, which serves
    to share the correct menu for their country and to identify the person
    who places the order

    Note
    ------
    slack_id is mandatory as it is used when sending notifications to the
    employee.
    """

    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    country = models.CharField(
        _("country"),
        max_length=2,
        choices=ENABLED_COUNTRIES,
        db_index=True,
        help_text=_("Country where the employee currently works.")
    )
    slack_id = models.CharField(
        _("slack member id"),
        unique=True,
        max_length=20,
        db_index=True
    )

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    def clean(self):
        super().clean()
        # Remove empty spaces from employee names and apply formatting
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().title()

    def get_full_name(self):
        # Returns the union of the employee's first name and last name.
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # Returns the employee's first name.
        return self.first_name.split()[0]

    def __str__(self):
        return self.get_full_name()