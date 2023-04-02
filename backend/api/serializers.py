import base64
import re

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from bookmarks.models import BookMark, ShoppingCart
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from subscription.models import Follow
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)

        return super().to_internal_value(data)


class BookMarkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = BookMark
        fields = ['id', 'name', 'image', 'cooking_time']

    def validate(self, attrs):
        recipe_obj = get_object_or_404(
            Recipe,
            id=self.context.get(
                'request').parser_context.get('kwargs').get('pk'))

        if recipe_obj in self.context.get('favorites'):
            raise serializers.ValidationError('Этот рецепт у вас уже есть')

        attrs.update({'user': self.context.get('request').user,
                      'recipe': recipe_obj})
        return attrs

    def get_name(self, obj):
        return obj.recipe.name

    def get_image(self, obj):
        uri = self.context.get('request').build_absolute_uri()
        image_prefix = re.findall('.*api/', uri)[0].rstrip('api/') + '/media/'
        return image_prefix + str(obj.recipe.image)

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time


class ShoppingCartSerializer(BookMarkSerializer):
    class Meta:
        model = ShoppingCart
        exclude = ['recipe', 'user', 'id']


class IngredientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id',
                  'name',
                  'measurement_unit']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id',
                  'name',
                  'color',
                  'slug']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit', 'amount']

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_amount(self, obj):
        return obj.amount


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.SerializerMethodField()
    ingredients = IngredientRecipeSerializer(many=True,
                                             read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        return obj.id in self.context.get('favorites')

    def get_is_in_shopping_cart(self, obj):
        return obj.id in self.context.get('shopping_cart')

    def get_author(self, obj):
        return UserGetSerializer(
            instance=obj.author,
            context=self.context).data


class FollowRecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']

    def get_image(self, obj):
        return self.context.get('prefix') + obj.get('image')


class FollowGetSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count']

    def get_email(self, obj):
        return obj.author.email

    def get_id(self, obj):
        return obj.author.id

    def get_username(self, obj):
        return obj.author.username

    def get_first_name(self, obj):
        return obj.author.first_name

    def get_last_name(self, obj):
        return obj.author.last_name

    def get_is_subscribed(self, obj):
        subscriptions = Follow.objects.filter(
            user_id=self.context.get(
                'request').user).values_list('author_id', flat=True)

        return obj.author.id in subscriptions

    def get_recipes(self, obj):
        uri = self.context.get('request').build_absolute_uri()
        image_prefix = re.findall('.*api/', uri)[0].rstrip('api/') + '/media/'
        return FollowRecipeSerializer(
            many=True,
            instance=Recipe.objects.filter(author=obj.author).values(),
            context={'prefix': image_prefix}).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        exclude = ['user', 'author', 'id']

    def to_representation(self, instance):
        return FollowGetSerializer(instance=instance,
                                   context=self.context).data

    def validate(self, attrs):
        a_user = self.context.get('request').user
        author = get_object_or_404(
            User,
            id=self.context.get(
                'request').parser_context.get('kwargs').get('pk'))

        if author == a_user:
            raise serializers.ValidationError('Нельзя подписаться на себя')

        if author.id in self.context.get('subscriptions'):
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора')

        attrs.update({'user': a_user,
                      'author': author})

        return attrs


class TagField(serializers.Field):
    def to_internal_value(self, data):
        return Tag.objects.filter(id__in=data)

    def to_representation(self, value):
        return value.values()


class RecipePostSerializer(RecipeGetSerializer):
    image = Base64ImageField()
    tags = TagField()
    author = serializers.CharField(required=False)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = self.initial_data.get('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)
        new_recipe.tags.set(tags)

        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                recipe=new_recipe,
                ingredient=Ingredient.objects.get(id=values.get('id')),
                amount=values.get('amount')) for values in ingredients])

        new_recipe.save()
        return new_recipe

    def update(self, instance, validated_data):
        if 'ingredients' in self.initial_data:
            instance.ingredients.all().delete()
            ingredients = self.initial_data.get('ingredients')

            IngredientRecipe.objects.bulk_create([
                IngredientRecipe(
                    recipe=instance,
                    ingredient=Ingredient.objects.get(id=values.get('id')),
                    amount=values.get('amount')) for values in ingredients])

        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed']

    def get_is_subscribed(self, obj):
        if 'subscriptions' in self.context:
            return obj.id in self.context.get('subscriptions')
        return False


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password']

    def to_representation(self, instance):
        return UserGetSerializer(instance=instance).data

    def create(self, validated_data):
        user = User(email=validated_data.get('email'),
                    username=validated_data.get('username'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'))

        user.set_password(validated_data.get('password'))
        user.save()
        return user
