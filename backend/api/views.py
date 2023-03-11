from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User

from .serializers import UserGetSerializer, UserPostSerializer
from .serializers import logging

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()

#     def get_serializer_class(self):
#         logging.info(self)
#         if self.request.method == 'GET':
#             return UserGetSerializer
#         return UserPostSerializer