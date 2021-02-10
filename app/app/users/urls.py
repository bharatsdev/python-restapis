from django.urls import path
from .views import CreateUserViewSets, CreateTokenViewSets

app_name = "users"

urlpatterns = [
    path("create/", CreateUserViewSets.as_view(), name="create"),
    path("token/", CreateTokenViewSets.as_view(), name="token")
]
