from django.contrib import admin

from bookmarks.models import BookMark, ShoppingCart
from recipes.models import Ingredient, Recipe, Tag
from subscription.models import Follow

from .models import User

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Follow)
admin.site.register(BookMark)
admin.site.register(ShoppingCart)
