from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', ]
        read_only_fields = ['id', ]
