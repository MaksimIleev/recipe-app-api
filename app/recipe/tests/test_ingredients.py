"""
Tests for ingredients API.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    Ingredient,
    Recipe,
)

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_api(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='pass123'):
    """Create test user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientApiTests(TestCase):
    """Test unauthorized API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test authorized API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving ingredients."""
        Ingredient.objects.create(user=self.user, name="Lemon")
        Ingredient.objects.create(user=self.user, name="Pineapple")

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients returned are for the authenticated user."""
        user2 = create_user(email='user2@example.com', password='pass123')
        Ingredient.objects.create(user=user2, name="Lemon")
        ingredient = Ingredient.objects.create(
            user=self.user,
            name="Pineapple"
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating ingredients."""
        ingredient = Ingredient.objects.create(user=self.user, name="Lemon")

        payload = {'name': 'orange'}
        url = detail_api(ingredient.id)
        res = self.client.patch(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting ingredients."""
        ingredient = Ingredient.objects.create(user=self.user, name="Lemon")
        url = detail_api(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredient = Ingredient.objects.filter(id=ingredient.id)
        self.assertFalse(ingredient.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test filtering ingredients by assigned recipes."""
        ingredient = Ingredient.objects.create(user=self.user, name="Apples")
        ingredient2 = Ingredient.objects.create(user=self.user, name="Lemons")
        recipe = Recipe.objects.create(
            user=self.user,
            title='Apple Crumble',
            time_minutes=5,
            price=Decimal('10.00')
        )
        recipe.ingredients.add(ingredient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        serializer = IngredientSerializer(ingredient)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test filtering ingredients by assigned recipes."""
        ingredient = Ingredient.objects.create(user=self.user, name="Apples")
        Ingredient.objects.create(user=self.user, name="Lemons")
        recipe = Recipe.objects.create(
            user=self.user,
            title='Apple Crumble',
            time_minutes=15,
            price=Decimal('10.00')
        )
        recipe2 = Recipe.objects.create(
            user=self.user,
            title='Apple Pie',
            time_minutes=25,
            price=Decimal('14.00'),
        )
        recipe.ingredients.add(ingredient)
        recipe2.ingredients.add(ingredient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
