from rest_framework import serializers
import logging
from users.models import User


logging.basicConfig(
    filename='the_log.log',
    level=logging.DEBUG
	)


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
