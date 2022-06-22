from django.shortcuts import render

from api.models import Review, Comment, Genre, Category, Title
from rest_framework import permissions, viewsets
from .serializers import ReviewSerializer, CommentSerializer, GenreSerializer, CategorySerializer, TitleSerializer


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

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', ]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.admin)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', ]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.admin)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', ]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.admin)