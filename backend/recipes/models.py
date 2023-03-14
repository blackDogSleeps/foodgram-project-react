from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)
    recipe = models.ManyToManyField(
        'Recipe',
        through='IngredientRecipe',
        related_name='ingredients')

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               default=None)
    image = models.ImageField(upload_to='recipes/images/',
                              default=None)
    name = models.CharField(max_length=200,
                            default=None)
    text = models.TextField(default=None)
    cooking_time = models.IntegerField(default=1)


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    recipe = models.ManyToManyField('Recipe',
                                    through='TagRecipe',
                                    related_name='tags')

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)