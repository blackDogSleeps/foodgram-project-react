from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()

class BookMark(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE)

    user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE)

    def __str__(self):
    	return (f'Пользователь: {self.user} '
                f'Рецепт: {self.recipe}')


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_cart',
        on_delete=models.CASCADE)
    
    user = models.ForeignKey(
        User,
        related_name='shopping',
        on_delete=models.CASCADE)
    
    def __str__(self):
        return (f'Пользователь: {self.user} '
                f'Рецепт: {self.recipe}')