from django.conf.urls import url
from django.urls import path
from rest_framework_jwt import views as jwt_view

from . import views


urlpatterns = [
    path('register/', views.register),
    path('login/', jwt_view.obtain_jwt_token)
]
