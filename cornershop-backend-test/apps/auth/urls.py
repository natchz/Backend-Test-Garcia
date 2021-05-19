from django.urls import path
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path(_('logout'), auth_views.LogoutView.as_view(), name='logout'),
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
]