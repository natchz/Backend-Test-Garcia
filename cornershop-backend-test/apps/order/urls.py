from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

app_name = "order"

urlpatterns = [
    path("<uuid:pk>", order_customize, name="order-customize"),
]