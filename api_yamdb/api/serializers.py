from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from api.models import Comment, Review


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


# class SignupUserSerializer(serializers.ModelSerializer):
