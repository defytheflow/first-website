from django.urls import path

from .views import ProfilePage

urlpatterns = [
    path('', ProfilePage.as_view(), name='profile'),
]
