from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

#Clase para crear un usuario y/o sueperusuario
class MyAccountManager(BaseUserManager):
    #Funcion para crear un usuario simple 
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        #Definicion de un objeto de tipo user
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        #Creacion del password con el valor del parametro
        user.set_password(password)
        #Insercion del obejeto user a la base de datos
        user.save(using=self._db)
        return user

    #Funcion para crear un superuser
    def create_superuser(self, first_name, last_name, username, email, password):
        # Creacion del usuario
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Seteo de los atributos del admin
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        # Guardo el record
        user.save(using=self._db)
        return user



# Create your models here.
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #Campos por defecto que hay en Django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #Configuracion para iniciar sesion con email y no username
    USERNAME_FIELD = 'email'
    #Campos requeridos para el registro de un nuevo usuario
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Intanciamiento de la clase MyAccountManager()
    objects = MyAccountManager()

    #Listado de los registros en Django
    def __str__(self):
        return self.email
    
    #Verficiacion si el usuario tiene permisos de administradorm (Solo si el atributo is_admin es true)
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True