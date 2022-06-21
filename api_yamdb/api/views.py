from django.shortcuts import render

from api.models import Review, Comment
from users.models import User
from rest_framework import permissions, viewsets
from .serializers import ReviewSerializer, CommentSerializer
# from .permissions import SignupUserPermission
from rest_framework.permissions import AllowAny


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


class SignupUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)