from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    #Lista de propiedaes que se mostraran en el grid se account en Django
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    #Propiedad para linkear al detalle del usuario en cual queier columna
    list_display_links = ('email', 'first_name', 'last_name')
    # Campos de lectura de la ultima de fecha de conexion y fecha de creacion
    readonly_fields = ('last_login', 'date_joined')
    # Organizacion de forma acendente de la fecha de creacion del usuario
    ordering = ('date_joined',)

    # Iniciacion de variables
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Account, AccountAdmin)