from django.test import TestCase
from django.contrib.auth import get_user_model

from main_app import models


user_v = {
    'email': 'test1@mail.ru',
    'password': 'testpasword'
}


def sample_user(email=user_v['email'], password=user_v['password']):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_user_create_with_email(self):
        """
        Testing if uther with email is created
        """
        email = 'test@format.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertAlmostEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if email is normalized"""

        email = 'test@UPPERFORMAT.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())

    def test_new_user_ivalid_email(self):
        """Test if email is black that we need to raise any error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1')

    def test_create_new_suoeruser(self):
        """Test creating function new superuser"""

        user = get_user_model().objects.create_superuser(
            'test@format.com', '1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        # when we covert tag to string we assert its euql to name
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        # when we covert tag to string we assert its euql to name
        self.assertEqual(str(ingredient), ingredient.name)
