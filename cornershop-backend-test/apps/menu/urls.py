from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

app_name = "menu"

urlpatterns = [
    path(_("dish"), dish_list, name="dish-list"),
    path(_("dish/add"), dish_create, name="dish-create"),
    path(_("dish/<int:pk>/edit"), dish_edit, name="dish-edit"),
    path(_("add"), menu_create, name="menu-create"),
    path(_("<int:pk>/edit"), menu_edit, name="menu-edit"),
    path("<uuid:pk>", menu_order, name="menu-order"),
    path("", menu_list, name="menu-list"),
]