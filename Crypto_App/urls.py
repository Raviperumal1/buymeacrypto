from django.urls import path

from .import views

app_name='Crypto_App'

urlpatterns = [
    path('', views.index,name='index'),
]