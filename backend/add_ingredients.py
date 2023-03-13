from recipes.models import Ingredient

import os
import json

os.chdir('../data')
ingredients = json.load(open('ingredients.json', encoding='UTF-8'))

for i in ingredients:
     obj = Ingredient(name=i.get('name'),
     	              measurement_unit=i.get('measurement_unit'))
     if not Ingredient.objects.filter(name=obj.name).exists():
         obj.save()