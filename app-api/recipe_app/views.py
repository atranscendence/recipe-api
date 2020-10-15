from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from main_app.models import Tag, Ingredient
from recipe_app import serializers

# simple stadart django list model view


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the databse"""

    # check auth befor show any data

    permission_classes = {IsAuthenticated, }

    # if not self.request.user.is_superuser:
    authentication_classes = {TokenAuthentication, }

    queryset = Tag.objects.all()

    serializer_class = serializers.TagSerializer

    # ovewire creating function addnig new features
    def get_queryset(self):
        """Return objects for the curent authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # ovewire creating function addnig new features
    def perform_create(self, serializer):
        """Create a new tag"""
        # set user to auth user
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin
                        ):
    """Manage ingredients in the databse"""

    permission_classes = {IsAuthenticated, }
    #authentication_classes = {TokenAuthentication, }
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    # ovewire creating function addnig new features
    def get_queryset(self):
        """Return objects for the curent authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new ingredient"""
        serializer.save(user=self.request.user)
