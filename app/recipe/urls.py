from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSets, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register("tags", TagViewSets)
router.register("ingredient", IngredientViewSet)
router.register("recipe", RecipeViewSet)

app_name = "recipe"

urlpatterns = [
    path('', include(router.urls))
]
