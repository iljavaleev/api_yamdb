from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet, SignupUser,
                    CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    UsersViewSet, TokenUser)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoriesViewSet, basename='category')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
# router.register(r'signup', SignupUser, basename='signup')

auth_list = ("'signup/', SignupUser")

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', SignupUser),
    path('v1/auth/', include(auth_list)),
    path('v1/auth/token/', TokenUser)
]
