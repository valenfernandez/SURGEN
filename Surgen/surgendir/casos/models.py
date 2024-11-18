from email.policy import default
import magic
import os
from django.db import models
from django.utils.translation import gettext_lazy
from datetime import datetime  
from django.db.models.signals import pre_save, post_save
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group

# Create your models here.

class Provincias(models.TextChoices):
    # de acuerdo con ISO 3166-2:AR
    CABA                = "AR-C", gettext_lazy("CABA")
    BUENOS_AIRES        = "AR-B", gettext_lazy("Buenos Aires")
    CATAMARCA           = "AR-K", gettext_lazy("Catamarca")
    CHACO               = "AR-H", gettext_lazy("Chaco")
    CHUBUT              = "AR-U", gettext_lazy("Chubut")
    CORDOBA             = "AR-X", gettext_lazy("Córdoba")
    CORRIENTES          = "AR-W", gettext_lazy("Corrientes")
    ENTRE_RIOS          = "AR-E", gettext_lazy("Entre Ríos")
    FORMOSA             = "AR-P", gettext_lazy("Formosa")
    JUJUY               = "AR-Y", gettext_lazy("Jujuy")
    LA_PAMPA            = "AR-L", gettext_lazy("La Pampa")
    LA_RIOJA            = "AR-F", gettext_lazy("La Rioja")
    MENDOZA             = "AR-M", gettext_lazy("Mendoza")
    MISIONES            = "AR-N", gettext_lazy("Misiones")
    NEUQUEN             = "AR-Q", gettext_lazy("Neuquén")
    RIO_NEGRO           = "AR-R", gettext_lazy("Río Negro")
    SALTA               = "AR-A", gettext_lazy("Salta")
    SAN_JUAN            = "AR-J", gettext_lazy("San Juan",)
    SAN_LUIS            = "AR-D", gettext_lazy("San Luis")
    SANTA_CRUZ          = "AR-Z", gettext_lazy("Santa Cruz")
    SANTA_FE            = "AR-S", gettext_lazy("Santa Fe")
    SANTIAGO_DEL_ESTERO = "AR-G", gettext_lazy("Santiago del Estero",)
    TIERRA_DEL_FUEGO    = "AR-V", gettext_lazy("Tierra del Fuego")
    TUCUMAN             = "AR-T", gettext_lazy("Tucumán")
    # sin especificar
    SIN_ESPECIIFAR      = "None", gettext_lazy("(sin especificar)")


class Estados(models.TextChoices):
    ABIERTO            = "ABIERTO", ("En tramite")
    CERRADO            = "CERRADO", ("Archivado")

class Hijos(models.TextChoices):
    NC            = "NC", gettext_lazy("No corresponde")
    SI            = "SI", gettext_lazy("Si")
    NO            = "NO", gettext_lazy("No")

class Relaciones(models.TextChoices):
    FAMILIAR            = "FAMILIAR", gettext_lazy("Familiar")
    PAREJA            = "PAREJA", gettext_lazy("Pareja")
    EX_PAREJA            = "EX_PAREJA", gettext_lazy("Ex pareja")
    FAMILIAR_PAREJA            = "FAMILIAR_PAREJA", gettext_lazy("Familiar de la pareja")
    FAMILIAR_EX_PAREJA            = "FAMILIAR_EX_PAREJA", gettext_lazy("Familiar de la ex pareja")
    JEFE            = "JEFE", gettext_lazy("Jefe")
    VECINO            = "VECINO", gettext_lazy("Vecino")
    PROFESOR            = "PROFESOR", gettext_lazy("Profesor")
    PROPIETARIO            = "PROPIETARIO", gettext_lazy("Propietario del inmueble de residencia")
    COMPAÑERO            = "COMPAÑERO", gettext_lazy("Compañero")
    AMIGO            = "AMIGO", gettext_lazy("Amigo")
    OTRO            = "OTRO", gettext_lazy("OTRO")



class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Los usuarios deben tener un nombre de usuario')

        user = self.model( 
            username = username, 
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            username = username,
            password=password 
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Usuario', 
        max_length=125,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank = True, null= True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        permissions = self.get_group_permissions()
        if perm in permissions:
            return True
        else:
            if self.is_superuser:
                return True
            else:
                return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    
    

class Domicilio(models.Model):
    calle = models.CharField(max_length=100)
    altura = models.IntegerField()
    piso_depto = models.CharField(max_length=10, blank=True)
    codigo_postal = models.CharField(max_length=12, blank=True)
    localidad = models.CharField(max_length=100)
    provincia = models.CharField(
        max_length=4,
        choices=Provincias.choices,
        default=Provincias.SIN_ESPECIIFAR,
    )
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True)
    history = HistoricalRecords()
 
    def __str__(self):
        return (
            f"{self.calle} {self.altura}{f' ({self.piso_depto}) ' if self.piso_depto else ''}"
            f", {self.localidad}"
        )

        
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.DO_NOTHING) 
    documento = models.CharField(max_length=15, blank=True)  # cambiar a futuro? va con espacio y sin puntos: DNI 12345678
    telefono = models.CharField(max_length=24, blank=True)
    email = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Victima(Persona):
    usuario = models.OneToOneField(MyUser, null= True, on_delete=models.CASCADE)
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True, related_name='changed_by_user'), 
    history = HistoricalRecords()

def get_history_user(instance, **kwargs):
        return instance.changed_by


class Agresor(Persona):
    class Meta:
        verbose_name_plural = "Agresores"
    fecha_nacimiento = models.DateField(null=True, blank=True)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.DO_NOTHING, blank=True, null=True) 
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True, related_name='changed_by_user'), 
    history = HistoricalRecords()

class Contacto(models.Model):
    # muy muy técnicamente, es una Persona con menos atributos
    victima = models.ForeignKey(Victima, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=24)
    email = models.CharField(max_length=50, null=True, blank=True)
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True, related_name='changed_by_user'), 
    history = HistoricalRecords()
    def __str__(self):
        return self.nombre


#Un caso es una causa penal
class Caso(models.Model):
    class Meta:
        verbose_name = "Causa"
    victima = models.ForeignKey(Victima, on_delete=models.SET_NULL, null=True)
    agresor = models.ManyToManyField(Agresor)
    fecha = models.DateTimeField()
    estado = models.CharField(
        max_length=7,
        choices=Estados.choices,
        default=Estados.ABIERTO,
    )
    #  ipp = models.CharField(max_length=20)
    
    relacion = models.CharField(
        max_length=30,
        choices=Relaciones.choices,
        default=Relaciones.OTRO,
        verbose_name="Relacion",
    )
    hijos_en_comun = models.CharField(
        max_length=30,
        choices=Hijos.choices,
        default=Hijos.NC,
        verbose_name="Hijos en comun",
    )
    def __str__(self):
        agresores = "; ".join( str(a) for a in self.agresor.all() )
        return f"{self.victima}, agredida por {agresores}"


 #Una incidencia seria un tramite judcial que tiene asociados documentos.
class Incidencia(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=False)  # fecha denuncia/aviso/registro?
    descripcion = models.TextField()
    nombre = models.TextField() # ver si se deberia incluir o no
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True, related_name='changed_by_user'), 
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING, blank=True, null=True)
    fecha = models.DateTimeField(null=False)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="media")
    mimetype = models.CharField(max_length=256, blank=True, null=True) #https://stackoverflow.com/questions/643690/maximum-mimetype-length-when-storing-type-in-db
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True, related_name='changed_by_user'), 
    history = HistoricalRecords()
    def __str__(self):
        return os.path.basename(self.archivo.name)
    
def doc_mimetype(sender, created, instance , update_fields=["mimetype"], **kwargs):
    doc = Documento.objects.filter(id = instance.id)
    mime = magic.from_file(instance.archivo.path, mime=True)
    doc.update(mimetype = mime)

post_save.connect(doc_mimetype, sender=Documento)


class Concurrencia(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    fecha = models.DateTimeField(blank=True, default=datetime.now) 
    lugar_concurrido = models.TextField(verbose_name='Institucion concurrida')
    descripcion = models.TextField(blank=True, verbose_name= 'notas de operador')
    changed_by = models.ForeignKey('MyUser', on_delete=models.DO_NOTHING, blank=True, null= True, related_name='changed_by_user'), 
    history = HistoricalRecords()
    def __str__(self):
        return f" Concurrencia a {self.lugar_concurrido}"


