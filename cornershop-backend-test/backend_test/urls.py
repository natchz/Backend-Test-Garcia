"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from rest_framework import routers
from django.utils.translation import gettext_lazy as _
from apps.employee import views as employee_views
from apps.menu import views as menu_views
from apps.order import views as order_views
from .utils.healthz import healthz


# A router is instantiated to unify all end points of the api
router = routers.DefaultRouter()

"""
The api apps are registered with the following variables
( Url prefix, Viewset app, End point namespace )
"""
router.register("employee", employee_views.EmployeeViewSet, "employee")
router.register("menu", menu_views.MenuViewSet, "menu")
router.register("dish", menu_views.DishViewSet, "dish")
router.register("order", order_views.OrderViewSet, "order")

# All the actions of the api router will start with the url pattern 'app:'
urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/", include((router.urls, "api"))),
]

# Views that have translatable url and language prefix
urlpatterns += i18n_patterns(
    path(_("employee/"), include("apps.employee.urls")),
    path(_("menu/"), include("apps.menu.urls")),
    path(_("order/"), include("apps.order.urls")),
    path("", include("apps.auth.urls")),
    prefix_default_language=True
)