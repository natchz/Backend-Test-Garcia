from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from backend_test.utils.viewsets import SecureMultiSerializerModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from apps.order.models import Order
from .serializers import *
from .models import *

# Inherit from this class to implement more security
class MenuViewSet(SecureMultiSerializerModelViewSet):
    """
    This view will take care of all the end points of the api that may be
    related to the menu structure.
    """

    model = Menu

    # Allows multiple serializers, if the action is not in the dictionary,
    # it will be set to "default"
    serializers_list = {
        "default": MenuSerializer,
        "retrieve": MenuDetailSerializer,
    }

    # Limits the types of requests the view can make
    http_method_names = ["get", "post", "patch"]

    # Generate the queryset dynamically, here you can implement permissions
    # by object or relations with the authenticated user
    def get_queryset(self):
        queryset = Menu.objects.all()

        if self.action == "retrieve":
            return queryset.prefetch_related("dishes")

        return queryset.order_by("-pk")

    @action(methods=["post"], detail=True)
    def publish(self, request, pk=None):
        """
        Action to publish a menu to your employees
        """

        menu_object = self.get_object()

        if menu_object.is_published():
            return Response(
                {"detail": "The menu was previously published"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the start of the menu publication
        menu_object.set_publish()

        return Response(
            {"detail": "The menu was successfully published"},
            status=status.HTTP_200_OK
        )

# Inherit from this class to implement more security
class DishViewSet(SecureMultiSerializerModelViewSet):
    model = Dish

    # Allows multiple serializers, if the action is not in the dictionary,
    # it will be set to "default"
    serializers_list = {
        "default": DishSerializer,
    }

    # Limits the types of requests the view can make
    http_method_names = ["get", "post", "patch"]

    # Generate the queryset dynamically, here you can implement permissions
    # by object or relations with the authenticated user
    def get_queryset(self):
        return Dish.objects.all().order_by("-pk")

"""
Area for views that render HTML templates
"""

# Redirect the request to the correct view
def menu_order(request, pk):
    return redirect("order:order-customize", pk=pk)

@login_required
def menu_list(request):
    return render(request, "menu/menu-list.html")

@login_required
def menu_create(request):
    context = {
        "serializer": MenuSerializer,
    }
    return render(request, "menu/menu-create.html", context)

@login_required
def menu_edit(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    context = {
        "menu": menu,
        "serializer": MenuSerializer(menu),
    }
    return render(request, "menu/menu-edit.html", context)

@login_required
def dish_list(request):
    return render(request, "menu/dish-list.html")

@login_required
def dish_create(request):
    context = {
        "serializer": DishSerializer,
    }
    return render(request, "menu/dish-create.html", context)

@login_required
def dish_edit(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    context = {
        "dish": dish,
        "serializer": DishSerializer(dish),
    }
    return render(request, "menu/dish-edit.html", context)