""" Router for the API """

# Django
from django.urls import include, path

# DRF
from rest_framework.routers import DefaultRouter

# Views API
from Root.Users.api.views import UserViewSet

router = DefaultRouter()
router.register("user", UserViewSet, basename="users")
app_name = "users"

urlpatterns = [
    # API
    path("", include(router.urls)),
]
