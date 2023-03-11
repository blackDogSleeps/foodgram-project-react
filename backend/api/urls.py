from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import UserViewSet

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')
# router.register(r'users/me', UserViewSet, basename='users')

urlpatterns = [
    # path('', include(router.urls)),

    # path('users/me/', include('djoser.urls')),
    # path('users/set_password/', include('djoser.urls')),
    path('', include('djoser.urls.base')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))

]
