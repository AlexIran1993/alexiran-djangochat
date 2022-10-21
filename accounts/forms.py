from django import forms
from .models import Account

#Formulario para el registro de un nuevo usuario
class RegistrationForm(forms.ModelForm):

    # Cajas de texto para el password y la confirmacion del password
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # Atributos de la caja de texto
        'placeholder': 'Ingrese password',
        'class': 'w-full mt-2 px-2 py-2 rounded-xl',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        # Atributos de la caja de texto
        'placeholder': 'Confirmar password',
        'class': 'w-full mt-2 px-2 py-2 rounded-xl',
    }))

    class Meta:
        #Modelo del que se basara mi formulario
        model = Account
        # Propiedades que tomare en cuenta del modelo Account para el registro de nuevos usuarios
        fields = ['first_name', 'last_name','phone_number', 'email', 'password']

    # Asignacion de estilos a los campos
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese el nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingrese numero telefonico'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese el email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'w-full mt-2 px-2 py-2 rounded-xl'

    # Funcion para validar que el password se el mismo
    def clean(self):
        # Obtengo acceso a los datos del formulario
        cleaned_data = super(RegistrationForm, self).clean()
        # Extraigo los valores de password y confirm_password
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        # Validacion de los passwords
        if password != confirm_password:
            raise forms.ValidationError(
                "El password no coincide"
            )