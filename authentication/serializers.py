from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from authentication.models import User


class RegisterModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    role = CharField(write_only=True,required=False)
    class Meta:
        model = User
        fields = 'username','role', 'password', 'confirm_password'
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError('Passwords do not match')
        return data

    def save(self, **kwargs):
        password=self.validated_data['password']
        self.validated_data.pop('confirm_password')
        self.validated_data['password'] = make_password(password)
        return super(RegisterModelSerializer, self).save(**kwargs)


