from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet, CategoriesViewSet,
                    GenresViewSet, TitlesViewSet, UsersViewSet)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include('users.urls'))
]
