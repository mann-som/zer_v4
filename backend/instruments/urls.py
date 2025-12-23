from django.urls import path
from . import views

urlpatterns = [
    path("list_instruments/", views.list_instruments, name="list-instruments"),
    path("create/", views.create_instrument, name="create-instrument"),
    path("update/", views.update_instrument, name="update-instrument"),
    path("unlist/", views.delete_instrument, name="unlist-instrument"),
]
