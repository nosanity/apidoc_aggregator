from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        unti_auth = instance.social_auth.filter(provider='unti').first()
        return unti_auth and unti_auth.uid


class UserTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ['user', 'key']
