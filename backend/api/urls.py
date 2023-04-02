from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BookMarkViewSet, CustomUserViewSet,
                    DownloadShoppingCartView, FollowViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingCartViewSet, TagViewSet)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')

subscriptions_list = FollowViewSet.as_view({'get': 'list'})
subscription_create_destroy = FollowViewSet.as_view({'post': 'create',
                                                     'delete': 'destroy'})
bookmark_create_destroy = BookMarkViewSet.as_view({'post': 'create',
                                                   'delete': 'destroy'})
shopping_create_destroy = ShoppingCartViewSet.as_view({'post': 'create',
                                                       'delete': 'destroy'})
download_shopping_list = DownloadShoppingCartView.as_view()


urlpatterns = [
    path('recipes/download_shopping_cart/',
         download_shopping_list,
         name='download-shopping-cart'),

    path('recipes/<int:pk>/shopping_cart/',
         shopping_create_destroy,
         name='shopping'),

    path('recipes/<int:pk>/favorite/',
         bookmark_create_destroy,
         name='favorite'),

    path('users/<int:pk>/subscribe/',
         subscription_create_destroy,
         name='subscribe'),

    path('users/subscriptions/',
         subscriptions_list,
         name='subscriptions'),

    path('', include(router.urls)),
    # path('', include('djoser.urls.base')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
