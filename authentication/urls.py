
from django.urls import path

from authentication.views import RegistrationAPiView

urlpatterns = [
    path('register/', RegistrationAPiView.as_view(),name='register'),
]
