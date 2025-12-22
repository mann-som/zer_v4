from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register-user"),
    path("get_user/", views.UserListView.as_view(), name="get-user"),
    path("update_email/", views.update_email, name="update-email"),
    path("update_name/", views.update_name, name="update-name"),
    path("update_mobile/", views.update_mobile, name="update-mobile"),
    path("delete/", views.delete_user, name="delete-user"),
]