from django.urls import path

from api.views import SignupUser, TokenUser


urlpatterns = [
    path('signup/', SignupUser),
    path('token/', TokenUser),
]
