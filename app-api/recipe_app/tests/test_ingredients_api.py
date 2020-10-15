from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from main_app.models import Ingredient

from recipe_app.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe_app:ingredient-list')

user_v = {
    'email': 'test1@mail.ru',
    'password': 'testpasword'
}


def sample_user(email=user_v['email'], password=user_v['password']):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicIngredientsTests(TestCase):
    """Test publicly awalible ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to ascces the endpoint"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient_list(self):
        """Test retriving a list of ingredients"""

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serilizer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returnd"""

        user2 = sample_user('other2@mail.ru', 'testdummy')

        Ingredient.objects.create(user=user2, name="Vine")

        ingredient = Ingredient.objects.create(user=self.user, name='Tur')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_succesfull(self):
        """Test create a new ingredient"""

        payload = {'name':'Cabbage'}
        self.client.post(INGREDIENTS_URL,payload)

        exist = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exist)

    
    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)