from rest_framework import viewsets, filters
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag
from users.models import User
from .permissions import AdminOrReadOnly, IsAuthorAdminOrReadOnly

from .serializers import (IngredientGetSerializer, RecipeGetSerializer,
                          RecipePostSerializer, TagSerializer,
                          UserGetSerializer, UserPostSerializer, logging)


class IngredientViewSet(viewsets.ModelViewSet):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientGetSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['^name']
	permission_classes = [AdminOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
	permission_classes = [AdminOrReadOnly]

