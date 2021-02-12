from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSets, IngredientViewSet

router = DefaultRouter()
router.register("tags", TagViewSets)
router.register("ingredient", IngredientViewSet)
app_name = "recipe"

urlpatterns = [
    path('', include(router.urls))
]
