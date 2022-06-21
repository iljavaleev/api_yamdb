from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet, SignupUserViewSet

router = DefaultRouter()


router.register(
     r'titles/(?P<title_id>[0-9]+)/reviews',
     ReviewViewSet,
     basename='reviews'
)
router.register(
     r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments/',
     CommentViewSet,
     basename='comments'
)

# router.register(r'auth/signup/', SignupUserViewSet, basename='signup')


urlpatterns = [
     path('v1/', include(router.urls)),
     path('v1/auth/signup/', SignupUserViewSet.as_view(), name='signup'),
     path('v1/', include('djoser.urls')),
     path('v1/', include('djoser.urls.jwt')),
]
