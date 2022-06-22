from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from api.models import Comment, Review, Title, Category, Genre
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
            )

    def get_rating(self, obj):
        return (
            Review.
            objects.
            filter(title=obj).
            aggregate(Avg('score'))['score__avg']
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
            ),
        )

class UserMeSerializer(serializers.ModelSerializer):
    # role = serializers.StringRelatedField(read_only=True)
    role = serializers.PrimaryKeyRelatedField(read_only=True)
    

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

        validators = (
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
            ),
        )



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')

        validators = [
            UniqueTogetherValidator(
                fields=('author', 'title_id'),
                queryset=Review.objects.all(),

            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
        read_only_fields = ('post',)


class SignupUserSerializer(serializers.Serializer):

    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Обязательные поля'
            ),
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('"me" — запретное имя пользователя')
        return data



class TokenUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = user.confirmation_code
        if data['confirmation_code'] != confirmation_code:
            raise serializers.ValidationError("Неверный код подтверждения")
        return data