from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient

from receipe.serializers import IngredientSerializer


INGREDIENT_URLS = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """Test the public available ingredient api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for access the endpoint"""
        res = self.client.get(INGREDIENT_URLS)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the private ingredient can be retrieved by authorized user"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredient"""
        Ingredient.objects.create(user=self.user, name='Spice')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENT_URLS)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'test1@gmail.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Vinigar')

        ingredient = Ingredient.objects.create(user=self.user, name='Tumaric')

        res = self.client.get(INGREDIENT_URLS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
