from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, RegisterView, TokenView

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenView.as_view(), name='token'),
    path('', include(router.urls)),
]