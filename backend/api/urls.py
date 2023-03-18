from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    FollowViewSet, FollowListViewSet, BookMarkViewSet)

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')

subscriptions_list = FollowViewSet.as_view({'get': 'list'})
subscription_create_destroy = FollowViewSet.as_view({'post': 'create',
                                                     'delete': 'destroy'})
bookmark_create_destroy = BookMarkViewSet.as_view({'post': 'create',
                                                   'delete': 'destroy'})



urlpatterns = [
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
    path('', include('djoser.urls.base')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
