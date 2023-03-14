from django.contrib import admin

from .models import User
from recipes.models import Ingredient, Recipe, Tag

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
