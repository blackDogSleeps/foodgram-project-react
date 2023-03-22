import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Добавляет ингридиенты и теги из папки "data" в базу данных'

    def handle(self, *args, **options):
        os.chdir('../data')
        ingredients_file = open('ingredients.json', encoding='UTF-8')
        tags_file = open('tags.json', encoding='UTF-8')

        ingredients = json.load(ingredients_file)
        tags = json.load(tags_file)

        ingredients_file.close()
        tags_file.close()

        for i in ingredients:
            obj = Ingredient(name=i.get('name'),
                             measurement_unit=i.get('measurement_unit'))
            if not Ingredient.objects.filter(name=obj.name).exists():
                print(obj)
                obj.save()

        for i in tags:
            obj = Tag(name=i.get('name'),
                      color=i.get('color'),
                      slug=i.get('slug'))
            if not Tag.objects.filter(name=obj.name).exists():
                print(obj)
                obj.save()
