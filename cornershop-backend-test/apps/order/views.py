from django.shortcuts import render, get_object_or_404
from backend_test.utils.viewsets import SecureMultiSerializerModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import *
from .models import *

# Inherit from this class to implement more security
class OrderViewSet(SecureMultiSerializerModelViewSet):
    """
    This view will take care of all the end points of the api that may be
    related to the order structure.
    """

    model = Order

    # Allows multiple serializers, if the action is not in the dictionary,
    # it will be set to "default"
    serializers_list = {
        "default": OrderSerializer,
        "list": OrderListSerializer,
        "retrieve": OrderDetailSerializer,
    }

    permissions_list = {
        # Security action is through knowledge of the uuid
        "retrieve": [],
        "partial_update": [],
    }

    access_list = {
        # These actions must be achieved without the need to be authenticated
        "retrieve": [AllowAny],
        "partial_update": [AllowAny],
    }

    # Implementation of generic filters for actions
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["menu"]

    # Limits the types of requests the view can make
    http_method_names = ["get", "patch"]

    # Generate the queryset dynamically, here you can implement permissions
    # by object or relations with the authenticated user
    def get_queryset(self):
        queryset = Order.objects.all()

        """
        The 'select_related' and 'prefetch_related' properties must be used
        in the queries that have some type of join or additional query
        """
        if self.action == "list":
            queryset.select_related("employee").prefetch_related("dishes")
        elif self.action == "retrieve":
            queryset.select_related("menu", "employee").prefetch_related("dishes")

        return queryset.order_by("-pk")

"""
Area for views that render HTML templates
"""

def order_customize(request, pk):
    order = get_object_or_404(Order, pk=pk)
    menu = order.menu

    context = {
        "order": order,
        "menu": menu,
        "dishes": menu.dishes.all()
    }
    return render(request, "order/order-customize.html", context)