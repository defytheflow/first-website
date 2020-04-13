from django.urls import path

from .views import ProfileView

urlpatterns = [
    path('<slug:username>', ProfileView.as_view(), name='profile'),
]
