from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from main_app.models import Recipe, Tag, Ingredient

from recipe_app.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe_app:recipe-list')

# /api/recipe/recipes
# /api/recipe/recipes/1/


def detail_url(recipe_id):
    """Return recipe detail URL"""
    # pss arg list b/c there can be multipe args for url
    return reverse('recipe_app:recipe-detail', args=[recipe_id])


def sample_tag(user, name='TagName'):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredinet(user, name='IngredinetName'):
    """Create and return sample tag"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create sample recipe"""

    # for more simple debuging
    defaults = {
        'title': "Sample recipe",
        'time_minutes': 10,
        'price': 5.00
    }
    # wich ever keys are in "defaults' will update from 'params'
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeTest(TestCase):
    """Test unatheticated recipe API acces"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that auth is requred to create recipe"""

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test untentificated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'Test@user.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_recipe_retriving(self):
        """Test that recipe can be created and info is corect"""
        sample_recipe(self.user)
        sample_recipe(self.user)
        res = self.client.get(RECIPES_URL)

        # get recipes we just created by the oder in wich they were created
        # that mean in revers by -
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retriving recipes are for user"""
        user2 = get_user_model().objects.create_user(
            "dummy@user.com",
            "pasword123"
        )

        sample_recipe(user=self.user)
        sample_recipe(user=user2)
        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredinet(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
