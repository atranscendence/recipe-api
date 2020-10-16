from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from main_app.models import Tag, Ingredient, Recipe
from recipe_app import serializers

# simple standart django list model view


class FondationAtributesViewSet(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin):
    "Base viewset that will use for Tags and Ingredinet for now"
    permission_classes = {IsAuthenticated, }  # IsAdminUser
    authentication_classes = {TokenAuthentication, }
    # if not self.request.user.is_superuser:

    # overwrite get function addnig new features
    def get_queryset(self):
        """Return objects for the curent authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # overwrite creating function addnig new features
    def perform_create(self, serializer):
        """Creating new object"""
        serializer.save(user=self.request.user)


class TagViewSet(FondationAtributesViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(FondationAtributesViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


# ModelViewSet for more flexible edeting
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the datase"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = {IsAuthenticated, }
    authentication_classes = {TokenAuthentication, }

    def get_queryset(self):
        """Retrive the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    # overwiriting serializer djnago class
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        else:
            return self.serializer_class
