"""Users URLs. / Templates URL's """

# Django
from django.urls import include, path

# Views
from Root.Users.views import LoginView, LogoutView, DashboardTemp

urlpatterns = [
    # Template
    path("login/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    # path("dashboard/", view=DashboardTemp.as_view(), name="temp"),
]
