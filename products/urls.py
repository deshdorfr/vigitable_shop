from django.urls import path
from .views import all_products, search_products

urlpatterns = [
    path("", all_products),
    path("search/", search_products),
]
