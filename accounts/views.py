from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

# Create your views here.
#Funcion para el registro de un nuevo usuario
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Creacion del usernamer usando el email.
            username = email.split("@")[0]            

            #Envio de datos a la funcion create_user el cual creara un objeto user que se registrara en la base de datos
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()

            #proceso de acticacion de usuario a travez del correo electronico
            #Sitio actual de la pagina
            current_site = get_current_site(request)
            #Titulo del correo electronico
            mail_subject = 'Activacion de cuenta para Djangochat'
            #Cuerpo del correo electronico
            body = render_to_string(
                #Template con el contenido del correo electronico
                'accounts/account_verification_email.html',{
                    #Valores dinamicos para el contenido del mensaje
                    #Usuario actual
                    'user': user,
                    #Dominio de la pagina actual
                    'domain': current_site,
                    #Primary key del usuario a dar de alta encifrando el pk del mismo
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    #Token que representara al mensaje
                    'token': default_token_generator.make_token(user),
                })
            
            #Envio del correo electronico
            to_email = email
            send_email = EmailMessage(
                #Titulo del email
                mail_subject,
                #Contenido del email
                body,
                #A quien va dirijido
                to=[to_email]
            )
            send_email.send()

            #Creacion de mensaje de exito
            #messages.success(request, 'El usuario se ha registrado exitosamente')
            #Redireccinamiento a la pagina register con el mensaje

            #Redireccionamineto a la pagina de login con el parametro command=verification y email=El email del usuario
            return redirect('/accounts/login/?command=varification&email='+email)

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

#Funcion para el login de un usuario registrado
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email, password = password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Inicio de sesion exitoso')
            return redirect('frontpage')
        else:
            messages.error(request, 'Las credenciales son incorrectas')
    return render(request, 'accounts/login.html')


#Funcion para salir de sesion
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Ha salido de sesion')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        #Decodificacion del pk del usuario
        uid = urlsafe_base64_decode(uidb64).decode()
        #Extraccion del usuario con el pk decodificado
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    #Validacion de que el usuario extraido anteriormente no sea nulo y que el token enviado como parametro coincida con la data del usuario
    if user is not None and default_token_generator.check_token(user, token):
        #Si la validacion es verdadera, cambio a True la propiedad is_active del usuario.
        user.is_active = True
        #Guradado de los cambios
        user.save()
        #Mensaje indicando la activacion del usuario
        messages.success(request,'Cuenta activada!')
        return redirect('login')
    else:
        messages.error(request,'Activacion invalida')
        return redirect('register')