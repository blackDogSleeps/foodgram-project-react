from django.db import models

class Recipe(models.Model):
	pass


class Ingredient(models.Model):
	name = models.CharField(unique=True, max_length=200)
	measurement_unit = models.CharField(max_length=200)
	recipe = models.ManyToManyField(
        'Recipe',
        through='IngredientRecipe',
        related_name='ingredient'
        )

class IngredientRecipe(models.Model):
	recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
	ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)

