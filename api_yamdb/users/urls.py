from django.urls import include, path

from api.views import SignupUser, TokenUser


urlpatterns = [
    path('signup/', SignupUser),
    path('token/', TokenUser),
]
