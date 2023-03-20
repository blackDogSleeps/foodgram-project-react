import logging

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from bookmarks.models import BookMark, ShoppingCart
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from subscription.models import Follow
from users.models import User


logging.basicConfig(
    filename='the_log.log',
    level=logging.INFO,
    filemode='w'
	)


class AuthorField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, obj):
        a_user = self.context.get('request').user
        logging.info(a_user.username)
        subscribed = False
        if a_user.username != '':
            subscribed = a_user.follower.filter(author=obj).exists()
        
        result = { 'email': obj.email,
                   'id': obj.id,
                   'username': obj.username,
                   'first_name': obj.first_name,
                   'last_name': obj.last_name,
                   'is_subscribed': subscribed }
        
        return result


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
        
        return super().to_internal_value(data)


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        exclude = ['recipe', 'user', 'id']

    def to_representation(self, data):
        self.fields = {
            'id': data.id,
            'name': data.recipe.name,
            'image': data.recipe.image.url,
            'cooking_time': data.recipe.cooking_time }
        return self.fields


class ShoppingCartSerializer(BookMarkSerializer):
    class Meta:
        model = ShoppingCart
        exclude = ['recipe', 'user', 'id']


class FollowGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


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


class IngredientsField(serializers.Field):
    def to_representation(self, data):
        keys = ['id', 'amount']
        result = []
        query = IngredientRecipe.objects.filter(
            recipe_id=data.instance.id).values()

        for item in query:
            new_item = {}
            for key, value in item.items():
                if key in keys:
                    new_item[key] = value
                elif key == 'ingredient_id':
                    ing_obj = Ingredient.objects.get(id=value)
                    new_item['name'] = ing_obj.name
                    new_item['measurement_unit'] = ing_obj.measurement_unit
            result.append(new_item)
        return result


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = AuthorField()
    ingredients = IngredientsField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        a_user = self.context.get('request').user
        if a_user.username != '':
            return obj.is_favorited.filter(user=a_user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        a_user = self.context.get('request').user
        if a_user.username != '':
            return obj.is_in_shopping_cart.filter(user=a_user).exists()
        return False



class FollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Follow
        exclude = ['user', 'author', 'id']

    def to_representation(self, instance):
        user = instance.user
        author_fields = User.objects.get(id=instance.author_id).__dict__
        recipes = Recipe.objects.filter(author_id=instance.author_id)
        is_subscribed = user.follower.filter(
            author=instance.author).exists()
        result = {}
        keys = ['email',
                'id',
                'username',
                'first_name',
                'last_name']

        for key, value in author_fields.items():
            if key in keys:
                result[key] = value
        
        result.update({ 'is_subscribed': is_subscribed })
        result.update({ 'recipes': recipes.values('id',
                                                  'name',
                                                  'image',
                                                  'cooking_time') })
        result.update({ 'recipes_count': recipes.count() })
        return result


class TagField(serializers.Field):
    def to_internal_value(self, data):
        data = Tag.objects.filter(id__in=data)
        return data

    def to_representation(self, value):
        return value.values()


class RecipePostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)
    tags = TagField()
    author = AuthorField(required=False)
    ingredients = IngredientsField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)
        new_recipe.tags.set(tags)

        for values in ingredients:
            ingredient_obj = IngredientRecipe(
                recipe=new_recipe,
                ingredient=Ingredient.objects.get(id=values.get('id')),
                amount=values.get('amount'))
            ingredient_obj.save()
        new_recipe.save()
        return new_recipe


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
        a_user = self.context.get('request').user
        if a_user.username == '':
            return False
        return a_user.follower.filter(author=obj).exists()


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'id', 
                  'username',
                  'first_name',
                  'last_name',
                  'password']
    
    def to_representation(self, data):
        result = {}
        for key, value in data.__dict__.items():
            if key in self.fields.keys() and key != 'password':
                result.update({ key: value })
        return result

    def create(self, validated_data):
        user = User(email=validated_data.get('email'),
                    username=validated_data.get('username'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'))
        
        user.set_password(validated_data.get('password'))
        user.save()
        return user
