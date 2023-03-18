from django.contrib import admin

from .models import User
from recipes.models import Ingredient, Recipe, Tag
from subscription.models import Follow
from bookmarks.models import BookMark, ShoppingCart

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Follow)
admin.site.register(BookMark)
admin.site.register(ShoppingCart)