from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookMark, ShoppingCart
from recipes.models import Ingredient, Recipe, Tag
from subscription.models import Follow

from .exceptions import SameSubscribe
from .filters import RecipeFilter
from .make_pdf import make_pdf
from .permissions import AdminOrReadOnly, IsAuthorAdminOrReadOnly
from .serializers import (BookMarkSerializer, FollowSerializer,
                          IngredientGetSerializer, RecipeGetSerializer,
                          RecipePostSerializer, ShoppingCartSerializer,
                          TagSerializer, UserGetSerializer, UserPostSerializer)


class DownloadShoppingCartView(APIView):
    def get(self, request):
        result = {}
        cart = request.user.shopping.all()
        for position in cart:
            for item in position.recipe.ingredients.all():
                if item.ingredient.name in result:
                    value = result.get(item.ingredient.name)
                    value[-1] += item.amount
                    result.update({item.ingredient.name: value})
                else:
                    result[item.ingredient.name] = [
                        item.ingredient.measurement_unit,
                        item.amount]

        return FileResponse(make_pdf(result),
                            as_attachment=True,
                            filename='shopping-cart.pdf')


class ShoppingCartViewSet(CreateModelMixin,
                          DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'favorites': BookMark.objects.filter(
                user_id=self.request.user).values_list(
                    'recipe_id', flat=True)}

    def perform_create(self, serializer):
        a_user = self.request.user
        recipe_obj = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if a_user.shopping.filter(recipe=recipe_obj).exists():
            raise SameSubscribe('Этот рецепт уже в корзине')
        serializer.save(user=a_user, recipe=recipe_obj)

    def destroy(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            request.user.shopping,
            recipe_id=self.kwargs.get('pk'))
        subscription.delete()
        return Response(
            {"detail": 'Рецепт удален из корзины'},
            status=status.HTTP_204_NO_CONTENT)


class BookMarkViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'favorites': BookMark.objects.filter(
                user_id=self.request.user).values_list('recipe_id', flat=True)}

    def destroy(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            request.user.likes,
            recipe_id=self.kwargs.get('pk'))
        subscription.delete()
        return Response(
            {"detail": 'Рецепт удален из закладок'},
            status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscriptions': Follow.objects.filter(
                user_id=self.request.user).values_list('author_id', flat=True)}

    def destroy(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            request.user.follower,
            author_id=self.kwargs.get('pk'))
        subscription.delete()
        return Response(
            {"detail": ('Вы успешно отписались '
                        f'от автора {subscription.author}')},
            status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientGetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
    permission_classes = [AdminOrReadOnly]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'favorites': BookMark.objects.filter(
                user_id=self.request.user).values_list('recipe_id', flat=True),

            'subscriptions': Follow.objects.filter(
                user_id=self.request.user).values_list('author_id', flat=True),

            'shopping_cart': ShoppingCart.objects.filter(
                user_id=self.request.user).values_list('recipe_id', flat=True)}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = None


class CustomUserViewSet(UserViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserGetSerializer
        return UserPostSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscriptions': Follow.objects.filter(
                user_id=self.request.user).values_list('author_id', flat=True)}
