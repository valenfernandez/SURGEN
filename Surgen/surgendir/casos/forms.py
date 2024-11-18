from django import forms
from django.forms import DateField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from django.core.validators import validate_email 
from django.contrib.auth.models import User

from surgen import settings    
from .models import Concurrencia, Domicilio, Victima, Provincias, Caso, Documento, Contacto, Incidencia, Agresor



class PerfilForm(ModelForm):
	email = forms.EmailField(),
	telefono = forms.CharField(widget=forms.NumberInput),
	class Meta:
		model = Victima
		fields = ('email', 'telefono')
		labels = {
			'email': 'email',
			'telefono': 'telefono',	
		}
		widgets = {
		}

	def clean_email(self):
		email = self.cleaned_data.get("email")
		try:
			validate_email(email)
		except ValidationError as e:
			valid = False
		else:
			valid = True
		if not valid:
			raise forms.ValidationError("Email invalido: ejemplo@mail.com")
		return email

	def clean_telefono(self):
		telefono = self.cleaned_data.get("telefono")
		if not telefono.isdigit():
			raise forms.ValidationError("Telefono invalido, ingresar solo digitos numericos")
		return telefono


class DomicilioForm(ModelForm):
	
	provincia= forms.CharField(label='Provincia', widget=forms.Select(choices=Provincias.choices))
	class Meta:
		model = Domicilio
		fields = ('calle', 'altura', 'piso_depto', 'codigo_postal', 'localidad', 'provincia')
		labels = {
			'calle' :'Calle',
			'altura':'Altura', 
			'piso_depto':'Piso y Departamento', 
			'codigo_postal':'Codigo Postal',
			'localidad':'Localidad',
			'provincia':'',
		}
		widgets = {
			'calle': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Calle'}),
			'altura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Altura'}),
			'piso_depto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Piso-Departamento'}),
			'codigo_postal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Codigo postal'}),
			'localidad': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Localidad'}),
		}
	def clean_piso_depto(self): #ver que pasa si lo deja vacio.
		piso_depto = self.cleaned_data.get("piso_depto")
		if piso_depto :
			if ' ' in piso_depto:
				piso, depto = piso_depto.split(' ')
			else: 
				piso = piso_depto
			if not piso.isdigit():
				raise forms.ValidationError("Numero invalido. Formato requerido: 1 A / 101")
		return piso_depto
	
	def clean_codigo_postal(self): #ver que pasa si lo deja vacio.
		codigo_postal = self.cleaned_data.get("codigo_postal")
		if not codigo_postal.isdigit():
			raise forms.ValidationError("Numero invalido.")
		return codigo_postal


class ContactoForm(ModelForm):
	email = forms.EmailField(),
	class Meta:
		model = Contacto
		fields = ('nombre', 'email', 'telefono')
		labels = {
			'nombre': 'Nombre',
            'email': 'Email',
			'telefono': 'Telefono',
				
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
			'telefono': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono'}),
		}
	def clean_email(self):
		email = self.cleaned_data.get("email")
		if email:
			try:
				validate_email(email)
			except ValidationError as e:
				valid = False
			else:
				valid = True
			if not valid:
				raise forms.ValidationError("Email invalido: ejemplo@mail.com")
		return email
		
	def clean_telefono(self):
		telefono = self.cleaned_data.get("telefono")
		if not telefono.isdigit():
			raise forms.ValidationError("Telefono invalido, ingresar solo digitos numericos")
		return telefono

class DateInput(forms.DateInput):
	input_type = 'date'
	date_effet = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), label='Date effet')


class ConcurrenciaForm(ModelForm):
	class Meta:
		model = Concurrencia
		fields = ('lugar_concurrido', 'descripcion')
		labels = {
			'lugar_concurrido': '',
			'descripcion': '',	
		}
		widgets = {
			'lugar_concurrido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lugar concurrido'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nota'}),
		}


class DocumentoForm(ModelForm):

	def __init__(self, *args, **kwargs):
		caso = kwargs.pop('caso', False)
		incidencias = Incidencia.objects.filter(caso = caso)
		super(DocumentoForm, self).__init__(*args, **kwargs)
		self.fields['incidencia'] = forms.ModelChoiceField(
                required=False,
                queryset=Incidencia.objects.filter(caso = caso),
                widget=forms.Select(choices = incidencias), 
				label='Tramite judicial')
	#fecha = DateField(input_formats=settings.DATE_INPUT_FORMATS)
	class Meta:
		model = Documento
		fields = ('fecha', 'descripcion', 'archivo')
		labels = {
			'fecha': '',
			'descripcion': '',
			'archivo': '',	
		}
		widgets = {
			'fecha': DateInput(attrs={'class':'form-control', 'placeholder':'Fecha'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
			'archivo': forms.ClearableFileInput(attrs={'class':'form-control', 'placeholder':'Archivo'}),
		}
	
	


class IncidenciaForm(ModelForm):
	#fecha = DateField(input_formats=settings.DATE_INPUT_FORMATS)
	class Meta:
		model = Incidencia
		fields = ('fecha', 'nombre', 'descripcion')
		labels = {
			'fecha': '',
			'nombre': '',	
			'descripcion': '',
		}
		widgets = {
			'fecha': DateInput(attrs={'class':'form-control', 'placeholder':'Fecha'}),
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
		}


class AgresorCasoForm(ModelForm): #En realidad son dos datos del caso que refieren al agresor
	class Meta:
		HIJOS_CHOICES =(
		("NC","NC"),
		("SI","SI"),
		("NO","NO"),
		)
		RELACIONES_CHOICES = (
			("FAMILIAR", "FAMILIAR"),
			("PAREJA", "PAREJA"),
			("EX_PAREJA", "EX_PAREJA"),
			("FAMILIAR_PAREJA", "FAMILIAR_PAREJA"),
			("FAMILIAR_EX_PAREJA", "FAMILIAR_EX_PAREJA"),
			("JEFE", "JEFE"),
			("VECINO", "VECINO"),
			("PROFESOR", "PROFESOR"),
			("PROPIETARIO", "PROPIETARIO"),
			("COMPAÑERO", "COMPAÑERO"),
			("AMIGO", "AMIGO"),
			("OTRO", "OTRO"),
		)
		model = Caso
		fields = ('relacion', 'hijos_en_comun')
		labels = {
			'relacion': 'Relacion',
			'hijos_en_comun': 'Hijos en comun',	
		}
		widgets = {
			'relacion': forms.Select(choices = RELACIONES_CHOICES ,attrs={'class':'form-control', 'placeholder':'Relacion'}),
			'hijos_en_comun': forms.Select(attrs={'class':'form-control', 'choices' : HIJOS_CHOICES, 'placeholder':'Hijos en Común'}),
		}

class AgresorForm(ModelForm):
	email = forms.EmailField(),
	class Meta:
		model = Agresor
		fields = ('telefono','email')
		labels = {	
			'telefono': 'Telefono',
			'email': 'Correo electronico',
		}
		widgets = {
			'telefono': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono'}),
		}
	
	def clean_email(self):
		email = self.cleaned_data.get("email")
		try:
			validate_email(email)
		except ValidationError as e:
			valid = False
		else:
			valid = True
		if not valid:
			raise forms.ValidationError("Email invalido: ejemplo@mail.com")
		return email
		
	def clean_telefono(self):
		telefono = self.cleaned_data.get("telefono")
		if not telefono.isdigit():
			raise forms.ValidationError("Telefono invalido, ingresar solo digitos numericos")
		return telefono
    

# forms.py

class registro_form(UserCreationForm):
    username = forms.CharField(label='Usuario', min_length=5, max_length=150)  
    email = forms.EmailField(label='E-mail')  
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("Usuario ya existe en el sistema")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email ya existe en el sistema")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Las contraseñas no coinciden")  
        return password2  
  
    def save_m2m(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  
