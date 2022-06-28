from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import Comment, Review, Title, Category, Genre

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class TitlesField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {"name": value.name, "slug": value.slug}


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    genre = TitlesField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    category = TitlesField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


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
        author = self.context.get('request').user

        if (Review.objects.filter(title_id=title_id, author=author).exists()
                and not self.partial):
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв'
            )

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
            raise serializers.ValidationError(
                '"me" — запретное имя пользователя'
            )

        if len(data['username']) < 3:
            raise serializers.ValidationError(
                'слишком короткое имя пользователя'
            )

        if User.objects.filter(email=data['email']).exists():
            if not User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('такой email уже существует')

        if User.objects.filter(username=data['username']).exists():
            if not User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError(
                    'такой username уже существует'
                )

        return data

    class Meta:
        fields = ('username', 'email')


class TokenUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
