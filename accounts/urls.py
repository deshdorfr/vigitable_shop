from django.urls import path
from .views import (
    signin_view,
    profile_view,
    update_profile_view,
    list_addresses,
    add_address,
    update_address,
    delete_address,
)

urlpatterns = [
    path("signin/", signin_view),

    path("profile/", profile_view),
    path("profile/update/", update_profile_view),

    path("addresses/", list_addresses),
    path("addresses/add/", add_address),
    path("addresses/<int:pk>/update/", update_address),
    path("addresses/<int:pk>/delete/", delete_address),
]
