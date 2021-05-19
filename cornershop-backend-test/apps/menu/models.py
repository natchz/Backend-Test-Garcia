import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from backend_test.choices import ENABLED_COUNTRIES, DISH_TYPES
from backend_test.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from . import tasks

# Inherit from this class to implement creation and modification track
class Menu(TimeStampedModel):
    """
    Unify a list of dishes in a structure that allows the assignment of
    date and geographic location of the menu to be published
    """

    date = models.DateField(
        _("date"),
        help_text=_("Date when the menu will be available.")
    )
    country = models.CharField(
        _("country"),
        max_length=2,
        choices=ENABLED_COUNTRIES,
        db_index=True,
        help_text=_("Country where the menu will be available.")
    )
    dishes = models.ManyToManyField("Dish", verbose_name=_("dishes"))
    time_limit = models.TimeField(
        _("time limit"),
        default=datetime.time(11, 00),
        help_text=_("Deadline to place an order.")
    )
    published = models.DateTimeField(
        _("published"),
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = _("menu")
        verbose_name_plural = _("menus")
        unique_together = ["date", "country"]

    def get_date_dict(self):
        # Returns a dictionary of the day and month of the menu.
        return {
            "month": self.date.strftime("%B"),
            "day": self.date.strftime("%d"),
        }

    def is_published(self):
        """
        Identify if the menu has already been previously published
        with the employees
        """
        return self.published is not None

    def set_publish(self):
        """
        Starts the asynchronous process of publishing the menu with all
        the employees of the respective country
        """

        #tasks.send_slack_notifications.apply_async(
        #    queue="celery",
        #    args=(self.pk,)
        #)
        tasks.send_slack_notifications(pk=self.pk)

        # The time of publication start is stored
        self.published = timezone.now()
        self.save()

    def __str__(self):
        return _("Menu of the day %(month)s %(day)s.") % self.get_date_dict()

# Inherit from this class to implement creation and modification track
class Dish(TimeStampedModel):
    """
    It allows to identify the type of each dish, in this way it is
    possible to validate the orders so that they only carry one dish
    of each type
    """

    name = models.CharField(_("name"), max_length=100)
    type = models.IntegerField(_("type"), choices=DISH_TYPES)

    class Meta:
        verbose_name = _("dish")
        verbose_name_plural = _("dishes")

    def __str__(self):
        return "%s: %s" % (self.get_type_display(), self.name)