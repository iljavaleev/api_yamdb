from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    permissions,
    viewsets,
    generics,
    status,
    filters,
    mixins
)

import uuid

from reviews.models import Review, Comment, Genre, Title, Category
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
    IsAuthenticatedPermission,
    IsAdminOrReadOnlyPermission,

)
from .filters import TitleFilter

User = get_user_model()


EMAIL = 'from@example.com'

class MixinSetList(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenresViewSet(MixinSetList):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    lookup_field = 'slug'
    ordering_fields = ('-id',)
    def get_permissions(self):
        if self.action in ['destroy','create']:
            permission_classes = [IsAdminOrReadOnlyPermission]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_permissions(self):
        if self.action in ['destroy','create']:
            permission_classes = [IsAdminOrReadOnlyPermission]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class CategoriesViewSet(MixinSetList):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    lookup_field = 'slug'
    ordering_fields = ('-id',)
    def get_permissions(self):
        if self.action in ['destroy','create']:
            permission_classes = [IsAdminOrReadOnlyPermission]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('-id',)
    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update', 'create']:
            permission_classes = [IsAdminOrReadOnlyPermission]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('-id',)
    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id).all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')),
        )

    def get_permissions(self):
        if self.action in ['destroy','update','partial_update']:
            permission_classes = [
                IsAuthorOrReadOnly | IsModeratorPermission | IsAdminPermission]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]


        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('-id',)
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
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [
                IsAuthorOrReadOnly | IsModeratorPermission | IsAdminPermission]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]


@api_view(['POST'])
@permission_classes([AllowAny])
def SignupUser(request):
    serializer = SignupUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, create = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response(
            'Такой логин или email уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Confirmation_code',
        f'Код подтверждения для {serializer.validated_data["username"]}: {confirmation_code}',
        EMAIL,
        (email, ),
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def TokenUser(request):
    serializer = TokenUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    current_user = get_object_or_404(User, username=username)
    if confirmation_code == current_user.confirmation_code:
        token = str(AccessToken.for_user(current_user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminPermission,)
    pagination_class = LimitOffsetPagination
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
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
