import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from rest_framework.response import Response

from api.models import Review, Comment
from users.models import User
from rest_framework import permissions, viewsets, generics, status
from .serializers import ReviewSerializer, CommentSerializer, SignupUserSerializer
# from .permissions import SignupUserPermission
from rest_framework.permissions import AllowAny

EMAIL = 'from@example.com'

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthorOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SignupUserViewSet(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupUserSerializer
    confirmation_code = str(uuid.uuid4())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        EmailMessage(
            'Confirmation_code',
            f'Код подтверждения: {self.confirmation_code}',
            EMAIL,
            (serializer.validated_data['email'],)
        ).send()
        serializer.save(
            confirmation_code=self.confirmation_code,
        )