from django.urls import path
from . import views

urlpatterns = [
    path('loby', views.rooms, name='rooms'),
    path('<slug:slug>/',views.room, name='room'),
    path('crear_chat', views.crear_chat, name='crearChat'),
    path('nuevo_chat', views.nuevochat, name='nuevochat')
]