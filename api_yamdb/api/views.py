import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination


from actions.models import Review, Comment, Genre, Title, Category
from users.models import User
from rest_framework import permissions, viewsets, generics, status, filters
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    SignupUserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
    UserMeSerializer,
    TokenUserSerializer
)
from .permissions import (
    IsAuthorOrReadOnly,
    IsModeratorPermission,
    IsAdminPermission,
    IsAuthenticatedPermission
)
# from .permissions import SignupUserPermission
from rest_framework.permissions import AllowAny

EMAIL = 'from@example.com'


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id).all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')),
        )

    def get_permissions(self):
        if self.action == 'delete':
            permission_classes = [
                IsAuthorOrReadOnly|IsModeratorPermission|IsAdminPermission]
        elif  self.action == 'update':
            permission_classes = [
                IsAuthorOrReadOnly | IsModeratorPermission | IsAdminPermission]
        permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return Comment.objects.filter(review=review).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=get_object_or_404(Review, id=self.kwargs.get(
                            'review_id')),
                        )

    def get_permissions(self):
        if self.action == 'delete':
            permission_classes = [
                IsAuthorOrReadOnly | IsModeratorPermission | IsAdminPermission]
        elif self.action == 'update':
            permission_classes = [
                IsAuthorOrReadOnly | IsModeratorPermission | IsAdminPermission]
        permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]


class SignupUserViewSet(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupUserSerializer
    confirmation_code = str(uuid.uuid4())

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(
    #         serializer.data,
    #         status = status.HTTP_200_OK
    #     )

    def perform_create(self, serializer):
        EmailMessage(
            'Confirmation_code',
            f'Код подтверждения для {serializer.validated_data["username"]}: {self.confirmation_code}',
            EMAIL,
            (serializer.validated_data['email'],)
        ).send()
        serializer.save(
            confirmation_code=self.confirmation_code,
        )


class TokenUserViewSet(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenUserSerializer

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        
        response = {'token': str(AccessToken.for_user(user))}
        return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminPermission,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticatedPermission,),
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if self.request.method == 'PATCH':
            self.partial_update(request)
            request.user.refresh_from_db()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
