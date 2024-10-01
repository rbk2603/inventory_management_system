from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer  # Create this serializer
from django.contrib.auth import authenticate  # Import authenticate


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        item = cache.get(f'item_{pk}')
        if not item:
            try:
                item = self.get_queryset().get(pk=pk)
                cache.set(f'item_{pk}', item, timeout=60 * 15)  # Cache for 15 minutes
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class TokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED)
