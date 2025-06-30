from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, get_csrf_token

router = DefaultRouter()
router.register(r'messages', ContactMessageViewSet, basename='contact-message')

urlpatterns = [
    path('', include(router.urls)),
    path('csrf/', get_csrf_token, name='get-csrf-token'),
]