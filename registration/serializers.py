from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import EmailField


class UserSerializer(serializers.ModelSerializer):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'email': {'required': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
