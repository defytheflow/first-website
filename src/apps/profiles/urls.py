from django.urls import path

from .views import ProfilePageView

urlpatterns = [
    path('', ProfilePageView.as_view(), name='profile'),
]
