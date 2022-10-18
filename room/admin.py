from django.contrib import admin
from .models import Room, Message
# Register your models here.

#Auto llenado del campo slug con la data de name / campos mostrados en el grid de Django
class RoomsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('invitado',)}
    list_display = ('creador','invitado','slug')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date_added')


admin.site.register(Room, RoomsAdmin)
admin.site.register(Message, MessageAdmin)