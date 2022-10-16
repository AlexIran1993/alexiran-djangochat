from django.shortcuts import render,redirect
from .models import Room, Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

# Create your views here.
@login_required(login_url='login')
def rooms(request):
    rooms = Room.objects.all()
    context={
        'rooms':rooms
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
    return render(request, 'rooms/newchat.html')

@login_required(login_url='login')
def nuevochat(request):
    nombre = request.POST['name']
    slug = re.sub(r"\s+", "-", nombre)
    room = Room.objects.filter(name=nombre)
    if room:
        messages.info(request, 'El chat con el nombre: ' + nombre + ', ya existe')
        return redirect('rooms')
    else:
        nuevo_room = Room.objects.create(name=nombre, slug=slug)
        nuevo_room.save()
        messages.success(request, 'El chat: ' + nombre + ', se ha creado con exito')
        return redirect('rooms')
