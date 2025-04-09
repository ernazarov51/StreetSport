from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import User


# Create your tests here.
@pytest.mark.django_db
class TestWordViewSet:

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_register(self,client):
        url=reverse('register')
        data={
            'username':'admin',
            'role':'admin',
            'password':'1',
            'confirm_password':'1'
        }
        response=client.post(url,data)
        assert response.status_code==201, f'Error, {response.content}'