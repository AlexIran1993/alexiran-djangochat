from datetime import datetime
from django.shortcuts import render,redirect
from .models import Room, Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from accounts.models import Account

# Create your views here.
@login_required(login_url='login')
def rooms(request):
    rooms = Room.objects.all()
    list_room = []
    for item in rooms:
        if item.creador == request.user.username or item.invitado == request.user.username:
            list_room.append(item)
            
    context={
        'rooms':list_room
    }
    return render(request,'rooms/rooms.html',context)

@login_required(login_url='login')
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    context = {
        'room':room,
        'messages': messages
    }
    return render(request, 'rooms/room.html', context)

@login_required(login_url='login')
def crear_chat(request):
    list_usuarios = Account.objects.filter(is_active=True)
    context = {
        'list_usuarios':list_usuarios
    }
    return render(request, 'rooms/newchat.html', context)

@login_required(login_url='login')
def nuevochat(request):
    creador = request.user.username
    invitado = request.POST["invitado"]

    if invitado == "null":
        list_usuarios = Account.objects.filter(is_active=True)
        context = {
            'list_usuarios':list_usuarios
        }
        messages.error(request, 'Seleccione un usuario de la lista')
        return render(request, 'rooms/newchat.html', context)


    slug = re.sub(r"[^\w\s]", "-", invitado)

    chat_creador = Room.objects.filter(creador=creador, invitado=invitado)
    chat_invitado = Room.objects.filter(creador=invitado, invitado=creador)

    if chat_creador or chat_invitado:
        messages.info(request, 'Ya tienes un canal con el usuario: ' + invitado)
        return redirect('rooms')
    else:
        print(invitado)
        print(creador)
        nuevo_room = Room.objects.create(slug=slug, creador=creador, invitado=invitado)
        nuevo_room.save()
        messages.success(request, 'Se ha creado un canal con el usuario: ' + invitado)
        return redirect('rooms')
