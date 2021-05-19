import uuid
from django.db import models
from apps.employee.models import Employee
from apps.menu.models import Menu, Dish
from backend_test.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

# Inherit from this class to implement creation and modification track
class Order(TimeStampedModel):
    """
    It allows the creation of a unique identifier for menu and employee,
    therefore it is possible to validate the authentication of the
    employee by the knowledge of this unique link
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name=_("menu"),
        on_delete=models.CASCADE,
        related_name="orders"
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name=_("employee"),
        on_delete=models.CASCADE,
        related_name="orders"
    )
    dishes = models.ManyToManyField(Dish, verbose_name=_("dishes"))
    note = models.CharField(
        _("note"),
        max_length=200,
        blank=True,
        help_text=_("Space to write the order customizations.")
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return _("%(employee)s's order for the menu of the day %(month)s %(day)s.") % {
            **self.menu.get_date_dict(),
            **{"employee": self.employee.get_short_name()}
        }