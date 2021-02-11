from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSets

router = DefaultRouter()
router.register("tags", TagViewSets)
app_name = "recipe"

print("************* Router Url****************")
print(router.urls)

urlpatterns = [
    path('', include(router.urls))
]
