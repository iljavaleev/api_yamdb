from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from actions.models import Comment, Review, Title, Category, Genre
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )
        lookup_field = 'slug'
        # extra_kwargs = {
        #     'slug': {'lookup_field': 'slug'}
        # }


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
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', )

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        author = self.context.get('request').user
        if self.partial or self.update:
            (Review.objects.filter(title=title, author=author)
             .update(text=data['text'], score=data['score']))
        elif Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы можете оставить только один отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', )


class SignupUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)


    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('"me" — запретное имя пользователя')
        
        elif User.objects.filter(email=data['email']).exists():
            if not User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('такой email уже существует')

        elif User.objects.filter(username=data['username']).exists():
            if not User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('такой username уже существует')   

        return data


    class Meta:
        fields = ('username', 'email')


class TokenUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')