from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
     ReviewViewSet,
     CommentViewSet,
     SignupUserViewSet,
     CategoriesViewSet,
     GenresViewSet,
     TitlesViewSet,
     UsersViewSet,
     TokenUserViewSet
)

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(
     r'titles/(?P<title_id>[0-9]+)/reviews',
     ReviewViewSet,
     basename='reviews'
)
router.register(
     r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
     CommentViewSet,
     basename='comments'
)
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
     path('v1/', include(router.urls)),
     path('v1/auth/signup/', SignupUserViewSet.as_view(), name='signup'),
     path('v1/auth/token/', TokenUserViewSet.as_view(), name='token'),
]
