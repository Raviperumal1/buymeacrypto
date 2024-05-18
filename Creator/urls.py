from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .import api

app_name='Creator'

urlpatterns = [
    path('api/create_support/',api.create_support,name='api_create_support'),
    path('creators/',views.creators,name='creators'),
    path('creators/<int:pk>/',views.creator,name='creator'),
    path('edit/',views.edit,name='edit'),
    path('mypage/',views.mypage,name='mypage'),
    path('signup/',views.signup,name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='Creator/login.html'),name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)