from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from authentication.models import User
from authentication.serializers import RegisterModelSerializer


# Create your views here.
@extend_schema(tags=['api'])
class RegistrationAPiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

