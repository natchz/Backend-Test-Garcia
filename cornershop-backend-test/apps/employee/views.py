from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from backend_test.utils.viewsets import SecureMultiSerializerModelViewSet
from .serializers import *
from .models import *

# Inherit from this class to implement more security
class EmployeeViewSet(SecureMultiSerializerModelViewSet):
    """
    This view will take care of all the end points of the api that may be
    related to the employee structure.
    """

    model = Employee

    # Allows multiple serializers, if the action is not in the dictionary,
    # it will be set to "default"
    serializers_list = {
        "default": EmployeeSerializer,
    }

    # Limits the types of requests the view can make
    http_method_names = ["get", "post", "patch"]

    # Generate the queryset dynamically, here you can implement permissions
    # by object or relations with the authenticated user
    def get_queryset(self):
        return Employee.objects.all().order_by("-pk")


"""
Area for views that render HTML templates
"""

@login_required
def employee_list(request):
    return render(request, "employee/employee-list.html")

@login_required
def employee_create(request):
    context = {
        "serializer": EmployeeSerializer,
    }
    return render(request, "employee/employee-create.html", context)

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    context = {
        "employee": employee,
        "serializer": EmployeeSerializer(employee),
    }
    return render(request, "employee/employee-edit.html", context)