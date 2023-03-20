from django.shortcuts import get_object_or_404
from django.http import FileResponse

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.mixins import (DestroyModelMixin, ListModelMixin,
                                   CreateModelMixin, RetrieveModelMixin)
from rest_framework.views import APIView

from bookmarks.models import BookMark, ShoppingCart
from recipes.models import Ingredient, Recipe, Tag
from subscription.models import Follow
from users.models import User
from .permissions import AdminOrReadOnly, IsAuthorAdminOrReadOnly

from .filters import RecipeFilter
from .make_pdf import make_pdf
from .exceptions import SelfSubscribe, SameSubscribe
from .serializers import (IngredientGetSerializer, RecipeGetSerializer,
                          RecipePostSerializer, TagSerializer,
                          UserGetSerializer, UserPostSerializer,
                          FollowGetSerializer, FollowSerializer,
                          BookMarkSerializer, ShoppingCartSerializer,
                          logging)


class DownloadShoppingCartView(APIView):
    def get(self, request):
        logging.info(self)
        logging.info(request.user)
        result = {}
        cart = request.user.shopping.all()
        for position in cart:
            for item in position.recipe.ingredients.all():
                if item.ingredient.name in result:
                    value = result.get(item.ingredient.name)
                    value[-1] += item.amount
                    result.update({ item.ingredient.name, value })
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
            {"detail": f'Рецепт удален из корзины'},
            status=status.HTTP_204_NO_CONTENT) 


class BookMarkViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer

    def perform_create(self, serializer):
        a_user = self.request.user
        recipe_obj = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if a_user.likes.filter(recipe=recipe_obj).exists():
            raise SameSubscribe('Этот рецепт у вас уже есть')
        serializer.save(user=a_user, recipe=recipe_obj)

    def destroy(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            request.user.likes,
            recipe_id=self.kwargs.get('pk'))
        subscription.delete()
        return Response(
            {"detail": f'Рецепт удален из закладок'},
            status=status.HTTP_204_NO_CONTENT)


class FollowListViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        a_user = self.request.user
        an_author = get_object_or_404(User, id=self.kwargs.get('pk'))
        if an_author == a_user:
            raise SelfSubscribe

        if a_user.follower.filter(author=an_author).exists():
            raise SameSubscribe
        
        serializer.save(user=self.request.user,
                        author=an_author)     


    def destroy(self, request, *args, **kwargs):
        subscription = get_object_or_404(
            request.user.follower,
            author_id=self.kwargs.get('pk'))
        subscription.delete()
        return Response(
            {"detail": f'Вы успешно отписались от автора {subscription.author}'},
            status=status.HTTP_204_NO_CONTENT)    
        

class IngredientViewSet(viewsets.ModelViewSet):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientGetSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['name']
	permission_classes = [AdminOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

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

