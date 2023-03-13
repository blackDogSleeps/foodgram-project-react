from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient

import os
import json

class Command(BaseCommand):
    help = 'Добавляет ингридиенты из папки "data" в базу данных'

    def handle(self, *args, **options):
        os.chdir('../data')
        ingredients = json.load(open('ingredients.json', encoding='UTF-8'))

        for i in ingredients:
            obj = Ingredient(name=i.get('name'),
                             measurement_unit=i.get('measurement_unit'))
            if not Ingredient.objects.filter(name=obj.name).exists():
                obj.save()

