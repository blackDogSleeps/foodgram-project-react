import logging

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


logging.basicConfig(
    filename='the_log.log',
    level=logging.DEBUG
	)


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


class IngredientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id',
                  'amount']



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id',
                  'name',
                  'color',
                  'slug']


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipePostSerializer(serializers.ModelSerializer):
    ingredient = 
    image = Base64ImageField(required=True, allow_null=False)
    tags = serializers.SlugRelatedField(many=True,
                                       queryset=Tag.objects.all(),
                                       slug_field='id')

    class Meta:
        model = Recipe
        fields = '__all__'


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
