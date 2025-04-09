"""
URL configuration for StreetSport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apps.views import StadiumCreateApiView, StadiumDetailApiView, SelfStadiumsOrderListApiView, \
    collect_manager_api_view, SavePlatformStadium, DeletePlatformStadium, get_stadium_count_api_view, \
    StadiumUpdateApiView, GetAllStadiums, BookingStadiums

urlpatterns = [
    path('owner/stadium/create/', StadiumCreateApiView.as_view(), name='stadium_create'),
    path('owner/stadium/stats/<int:pk>/', StadiumDetailApiView.as_view(), name='stadium_stats'),
    path('owner/booked/stadiums/', SelfStadiumsOrderListApiView.as_view(), name='stadium_order'),
    path('owner/collect/manager/<int:stadium_id>/', collect_manager_api_view, name='stadium_manager'),
    path('stadium/create/', SavePlatformStadium.as_view(), name='admin-platform-stadium'),
    path('stadium/delete/<int:pk>/', DeletePlatformStadium.as_view(), name='admin-platform-stadium'),
    path('stadium/count/', get_stadium_count_api_view, name='stadiums-count'),
    path('stadium/edit/<int:pk>/', StadiumUpdateApiView.as_view(), name='stadiums-edit'),
    path('user/get/stadiums/', GetAllStadiums.as_view(), name='all-stadiums'),
    path('user/booking/stadium/', BookingStadiums.as_view(), name='create-order'),
]

