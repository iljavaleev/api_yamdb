from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework.test import RequestsClient
from django.test import RequestFactory


from api.views import (
     ReviewViewSet,
     CommentViewSet,
     SignupUserViewSet,
     CategoriesViewSet,
     GenresViewSet,
     TitlesViewSet,
     UsersViewSet,
     TokenUserViewSet
)

User = get_user_model()

class ApiTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username='bingobongo',
                                       email='bingobongo@yamdb.fake',
                                       role=User.USER,
                                       )
        cls.moderator = User.objects.create(username='bingobongo1',
                                       email='bingobongo@yamdb.fake1',
                                       role=User.MODERATOR,
                                       )
        cls.admin = User.objects.create(username='bingobongo2',
                                       email='bingobongo@yamdb.fake2',
                                       role=User.ADMIN,
                                       )
        cls.admin.is_staff=True
        cls.super = User.objects.create_superuser(username='myuser',
                                                  email='myemail@test.com',
                                                  password='mypassword'
                                                  )

        cls.comment_url='http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/'
        cls.review_url = 'http://127.0.0.1:8000/api/v1/titles/1/reviews/'

        cls.factory = APIRequestFactory()


    def test_api_anon(self):
        request = ApiTests.factory.get(ApiTests.comment_url)
        view = CommentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = ApiTests.factory.get(ApiTests.review_url)
        view = CommentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)


        request = ApiTests.factory.get(ApiTests.comment_url)
        view = CommentViewSet.as_view({'get': 'retrieve'})
        response = view(request,comment_id=1)
        self.assertEqual(response.status_code, 200)

        request = ApiTests.factory.get(ApiTests.review_url)
        view = CommentViewSet.as_view({'get': 'retrieve'})
        response = view(request,review_id=1)
        self.assertEqual(response.status_code, 200)




    def test_moderator_api(self):
        user = ApiTests.moderator
        request = ApiTests.factory.get(ApiTests.comment_url)
        view = CommentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)



