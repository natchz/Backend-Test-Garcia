from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

app_name = "employee"

urlpatterns = [
    path(_("employee"), employee_list, name="employee-list"),
    path(_("employee/add"), employee_create, name="employee-create"),
    path(_("employee/<int:pk>/edit"), employee_edit, name="employee-edit"),
]