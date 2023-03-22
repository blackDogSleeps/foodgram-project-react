from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey('Recipe',
                               related_name='ingredients',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return (self.ingredient.name,
                self.amount)


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

    def __str__(self):
        return self.name


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
