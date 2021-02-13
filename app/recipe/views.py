from core import models
from recipe.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailsSerializer
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BaseRecipeViewSets(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base ViewSet for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns Objects  for the current authentication user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new Objects"""
        serializer.save(user=self.request.user)


class TagViewSets(BaseRecipeViewSets):
    """Manage tags in database"""
    serializer_class = TagSerializer
    queryset = models.Tag.objects.all()


class IngredientViewSet(BaseRecipeViewSets):
    """Manage Ingredients in Database"""
    queryset = models.Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage Recipes in Database"""
    queryset = models.Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate action class"""
        if self.action is 'retrieve':
            return RecipeDetailsSerializer
        return self.serializer_class
