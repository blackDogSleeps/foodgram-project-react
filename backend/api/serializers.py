import logging

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import User


logging.basicConfig(
    filename='the_log.log',
    level=logging.INFO,
    filemode='w'
	)


class AuthorField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        keys = ['email',
                'id',
                'username',
                'first_name',
                'last_name']
        result = {}
        
        for item in value.__dict__:
            if item in keys:
                result.update({ item: value.__dict__.get(item) })
        return result


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        return super().to_internal_value(data)


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


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = AuthorField()

    class Meta:
        model = Recipe
        fields = '__all__'


class TagField(serializers.Field):
    def to_internal_value(self, data):
        data = Tag.objects.filter(id__in=data)
        return data

    def to_representation(self, value):
        logging.info(value.values())
        return value.values()


class RecipePostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)
    tags = TagField()
    author = AuthorField(required=False)

    class Meta:
        model = Recipe
        fields = '__all__'

    # def create(self, validated_data):
    # #     ingredients = self._kwargs.get('data').get('ingredients')
        # logging.info(validated_data)
    #     tags = validated_data.pop('tags')
    #     validated_data.update({'author': author})
    #     new_recipe = Recipe.objects.create(**validated_data)
    #     new_recipe.tags.set(tags)
    # # logging.info(new_recipe.__dict__)
    #     for values in ingredients:
    #     # logging.info(values)
    #         ingredient_obj = IngredientRecipe(
    #             recipe=new_recipe,
    #             ingredient=Ingredient.objects.get(id=values.get('id')),
    #             amount=values.get('amount'))
    #         ingredient_obj.save()
    #     new_recipe.save()
    #     serializer.save(author=self.request.user)



class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'id', 
                  'username',
                  'first_name',
                  'last_name']


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'id', 
                  'username',
                  'first_name',
                  'last_name',
                  'password']

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user
