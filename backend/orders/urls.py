from django.urls import path
from . import views

urlpatterns = [
    path("place/", views.PlaceOrderView.as_view()),
    path("cancel/<int:order_id>/", views.CancelOrder.as_view()),
    path("", views.OrderListView.as_view()),
]
