from django_filters import rest_framework as djfilters
from recipes.models import Recipe


def return_bools(user_fav, value, queryset):
        if value == True:
            return queryset.filter(id__in=user_fav)
        return queryset.exclude(id__in=user_fav)


class RecipeFilter(djfilters.FilterSet):
    author = djfilters.CharFilter(field_name='author__username', lookup_expr='contains')
    tags = djfilters.CharFilter(field_name='tags__slug', lookup_expr='contains')
    is_favorited = djfilters.BooleanFilter(field_name='is_favorited', method='favorited')
    is_in_shopping_cart = djfilters.BooleanFilter(field_name='is_in_shopping_cart', method='shopping')

    def favorited(self, queryset, name, value):
        user_fav = self.request.user.likes.values('recipe_id')
        return return_bools(user_fav, value, queryset)

    def shopping(self, queryset, name, value):
        user_fav = self.request.user.shopping.values('recipe_id')
        return return_bools(user_fav, value, queryset)            
