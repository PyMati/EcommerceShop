from django.urls import path
from .views import *


urlpatterns = [
    path(
        "products/<int:product_id>/",
        name="product_details",
        view=GetSpecificProduct.as_view(),
    ),
    path("products/", name="product_operations", view=ProductOperations.as_view()),
    path("auth/", name="authentication", view=Auth.as_view()),
    path("order/", name="order_operations", view=OrderOperations.as_view()),
]
