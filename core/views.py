from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest
from .serializers import UserSerializer
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import  UserSerializer
from rest_framework import generics, filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import FriendRequestSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .serializers import UserSerializer




User = get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'email': token.user.email
        })

class UserSearchAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']
    # pagination_class = generics.pagination.PageNumberPagination
    # pagination_class.page_size = 10

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from_user = self.request.user
        to_user = serializer.validated_data['to_user']

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count()

        if recent_requests >= 3:
            return Response({"detail": "You have sent more than 3 friend requests in the last minute"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(from_user=from_user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.delete()
        return Response({"detail": "Friend request accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.delete()
        return Response({"detail": "Friend request rejected"}, status=status.HTTP_200_OK)
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from_user = self.request.user
        to_user = serializer.validated_data['to_user']

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count()

        if recent_requests >= 3:
            return Response({"detail": "You have sent more than 3 friend requests in the last minute"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(from_user=from_user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.delete()
        return Response({"detail": "Friend request accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.delete()
        return Response({"detail": "Friend request rejected"}, status=status.HTTP_200_OK)
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        from_user = self.request.user
        to_user = serializer.validated_data['to_user']

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user has sent more than 3 friend requests in the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count()

        if recent_requests >= 3:
            return Response({"detail": "You have sent more than 3 friend requests in the last minute"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(from_user=from_user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.delete()
        return Response({"detail": "Friend request accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.delete()
        return Response({"detail": "Friend request rejected"}, status=status.HTTP_200_OK)

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if '@' in query:  # Search by email
            return User.objects.filter(email__icontains=query)
        else:  # Search by name
            return User.objects.filter(username__icontains=query)

class FriendRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Check if user is trying to send more than 3 friend requests in a minute
        # Implement rate limiting logic here if required
        return super().post(request, *args, **kwargs)

class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))

class FriendRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class FriendRequestAcceptAPIView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.status = 'accepted'
        instance.save()

class FriendRequestRejectAPIView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.status = 'rejected'
        instance.save()



