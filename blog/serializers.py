from django.contrib.auth.models import User
from taggit.serializers import TaggitSerializer, TagListSerializerField
from rest_framework import serializers
from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'tags', 'status', 'author']



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class EditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'tags']

