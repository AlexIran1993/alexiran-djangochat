from django.contrib import admin
from .models import Room, Message
# Register your models here.

#Auto llenado del campo slug con la data de name / campos mostrados en el grid de Django
class RoomsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

admin.site.register(Room, RoomsAdmin)
admin.site.register(Message)