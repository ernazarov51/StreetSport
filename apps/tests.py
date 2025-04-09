import datetime

import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import User
from .models import Stadium, Order, PlatformStadium


# Create your tests here.
@pytest.mark.django_db
class TestWordViewSet:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        User.objects.create(password=make_password('1'), first_name='John', last_name='Doe', username='owner',
                            role='owner')
        User.objects.create(password=make_password('1'), first_name='John', last_name='Wick', username='admin',
                            role='admin', is_superuser=1)
        User.objects.create(password=make_password('1'), first_name='Ali', last_name='Valiyev', username='user',
                            role='user')
        User.objects.create(password=make_password('1'), first_name='Botir', last_name='Botirov', username='manager',
                            role='manager')
        Stadium.objects.create(name='Tashkent Stadium', region=Stadium.RegionChoices.yunusobod,
                               location_note='Bodomzor', owner_id=1, manager_id=2, price=150.00)
        PlatformStadium.objects.create(stadium_id=1)

    def test_create_station(self, client, db):
        url = reverse('token_obtain_pair')
        data = {'username': 'owner', 'password': '1'}
        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK, 'Login Error'

        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        url = reverse('stadium_create')
        data = {
            'name': 'Temp',
            'region': Stadium.RegionChoices.yunusobod,
            'location_note': 'Shaxristan',
            'price': 100
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, f"Error: {response.content}"

    def test_get_stadium_stats(self, client, db):
        url = reverse('token_obtain_pair')
        data = {'username': 'owner', 'password': '1'}
        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK, 'Login Error'

        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('stadium_stats', kwargs={'pk': 1})
        response = client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK, f'error: {response.content}'

    def test_get_bboked_stadiums(self, client, db):
        url = reverse('token_obtain_pair')
        data = {'username': 'owner', 'password': '1'}
        login_response = client.post(url, data)
        assert login_response.status_code == 200, 'Login Error!!!'
        access_token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('stadium_order')
        response = client.get(url)
        assert response.status_code == 200, 'Error!!!'

    def test_collect_manager(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'owner',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('stadium_manager', kwargs={'stadium_id': 1})
        data = {'manager_id': 4}
        response = client.post(url, format='json', data=data)
        assert response.status_code == 200, f'Error: {response.content}'

    def test_save_platform_stadium(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'owner',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('admin-platform-stadium')
        data = {
            'stadium': 1
        }
        assert response.status_code == 200, f'Error, {response.content}'

    def test_delete_platform_stadium(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('admin-platform-stadium', kwargs={'pk': 1})
        response = client.delete(url)
        assert response.status_code == 200, f'Error, {response.content}'

    def test_get_stadium_count(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('stadiums-count')
        response = client.get(url)
        assert response.status_code == 200, f'Error, {response.content}'

    def test_update_stadium(self, client,db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'owner',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('stadiums-edit', kwargs={'pk': 1})
        data = {
            'name': 'Hello World',
            'region': 'chilonzor',
            'location_note': 'chilonzor',
            'price': 100
        }
        response=client.put(url,data)
        assert response.status_code==200, f'Error, {response.content}'
        data = {
            'price': 150.00
        }
        response = client.patch(url, data)
        assert response.status_code == 200, f'Error, {response.content}'
    def test_get_all_stadiums(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'owner',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('all-stadiums')
        assert client.get(url).status_code==200, f"Error, {(client.get(url)).content}"

    def test_booking_stadium(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'owner',
            'password': 1
        }
        response = client.post(path=url, data=data)
        access_token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        url = reverse('create-order')
        data={
            'stadium':1,
            'start_time':'2024-04-10T14:30:00',
            'end_time':'2024-04-10T15:30:00'
        }
        response=client.post(url,data)
        assert response.status_code==201, f'Error!, {response.content}'
