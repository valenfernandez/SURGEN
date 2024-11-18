from fileinput import filename
import os
import mimetypes
import datetime
# from asyncio.windows_events import NULL
from re import search
from .models import Caso, Concurrencia, Domicilio, Victima, Incidencia, Documento, Contacto, Agresor
from .forms import DomicilioForm, PerfilForm, ContactoForm, ConcurrenciaForm, AgresorForm, IncidenciaForm, DocumentoForm, AgresorCasoForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.contrib import messages

# Create your views here.
@login_required
def perfil(request):
    if request.user.is_staff :
        response = redirect('/')
        return response
    else:
        victima = Victima.objects.get(usuario = request.user)
        context = {
            "victima": victima,
            "casos": Caso.objects.filter(victima = victima),
            "contactos": Contacto.objects.filter(victima = victima),
        }
        return render(request, "casos/perfil.html", context=context)

@login_required
def caso(request,id):
    if request.user.is_staff :
        response = redirect('/')
        return response
    else:
        caso = Caso.objects.get( id = id)
        caso_usuario = caso.victima.usuario
        if caso_usuario != request.user :
            response = redirect('/')
            return response
        else:
            agresores = caso.agresor.all()
            incidencias = Incidencia.objects.filter(caso = caso)
            documentos = Documento.objects.filter(caso = caso) 
            historial = []
            for inc in incidencias :
                historial.append({
                    'nombre': inc.nombre,
                    'fecha': inc.fecha,
                    'descripcion': inc.descripcion
                    }
                )
            for doc in documentos :
                historial.append({
                    'nombre': doc,
                    'fecha': doc.fecha,
                    'descripcion': doc.descripcion
                    }
                )
            concurrencias = Concurrencia.objects.filter(caso = caso)
            context = {
                "caso": caso, 
                "historial" : sorted(historial, key = lambda x: x['fecha']),
                "documentos" : documentos, 
                "agresores": agresores,
                "concurrencias": concurrencias,
            }
            return render(request, "casos/caso.html", context=context)

@login_required
def documentos(request,id_caso, id_doc):  
    if request.user.is_staff :
        response = redirect('/')
        return response
    else:
        try:
            caso = Caso.objects.get( id = id_caso)
            caso_usuario = caso.victima.usuario
            if caso_usuario != request.user :
                response = redirect('/')
                return response
            else:
                documentos = Documento.objects.filter(caso = caso) 
                file_content = ''
                if(id_doc != '-1'): # Si tengo un doc seleccionado para visualizar
                    doc_actual =  Documento.objects.get(id = id_doc)
                    filename = doc_actual.archivo.name
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    filepath = BASE_DIR +"/" + filename
                    if doc_actual.mimetype ==  "text/plain":
                        f = open(filepath, 'r')
                        file_content = f.read()
                        f.close()
                else:
                    doc_actual = '',
                    file_content = ''

                context = {
                    "caso": caso, 
                    "documentos" : documentos,
                    "doc_actual" : doc_actual,
                    'file_content': file_content,
                    'id_doc' :id_doc,
                }
                return render(request, "casos/documentos.html", context=context)
        except:
            response = redirect('/perfil/caso/documentos/'+ id_caso + '/-1')
            return response


def home(request): 

    if not request.user.is_authenticated:
        response = redirect('/login')
        return response
    else:
        if not request.user.is_staff: 
            response = redirect('/perfil')
            return response
        else: 
            return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html")

@login_required
def editar_perfil(request):
    if request.user.is_staff :
        response = redirect('/')
        return response
    else:
        victima = Victima.objects.get(usuario = request.user)
        domicilio = Domicilio.objects.get(victima = victima)
        form_perfil = PerfilForm(request.POST or None, request.FILES or None, instance=victima)
        form_domicilio = DomicilioForm(request.POST or None, request.FILES or None, instance=domicilio)
        context = {
            "form_perfil" : form_perfil,
            "form_domicilio" : form_domicilio,
        }
        if form_perfil.is_valid() and form_domicilio.is_valid():
            form_perfil.save()
            form_domicilio.save()
            response = redirect('/perfil')
            return response
        return render(request, "casos/editar_perfil.html", context = context)

@login_required
def agregar_contacto(request):
    if request.user.is_staff :
        response = redirect('/')
        return response
    else:
        victima = Victima.objects.get(usuario = request.user)
        contacto = Contacto(victima = victima, nombre ='', telefono='', email='')
        form_contacto = ContactoForm(request.POST or None, request.FILES or None, instance=contacto)
        context = {
            "form_contacto" : form_contacto,
        }
        if form_contacto.is_valid():
            form_contacto.save()
            response = redirect('/perfil')
            return response
        return render(request, "casos/agregar_contacto.html", context = context)

@login_required
def editar_contacto(request,id_contacto):
    if request.user.is_staff :
        response = redirect('/')
        return response
    else:
        victima = Victima.objects.get(usuario = request.user)
        contacto = Contacto.objects.get(victima = victima, id = id_contacto)
        form_contacto = ContactoForm(request.POST or None, request.FILES or None, instance=contacto)
        context = {
            "form_contacto" : form_contacto,
        }
        if form_contacto.is_valid():
            form_contacto.save()
            response = redirect('/perfil')
            return response
        return render(request, "casos/editar_contacto.html", context = context)

@login_required
def descargar(request, id_doc):
    doc =  Documento.objects.get(id = id_doc)
    filename = doc.archivo.name
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR +"/" + filename
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

@login_required
def operador_descargar_manual(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR +"/static/media/manual.pdf" 
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

@login_required
def descargar_pdf_concurrencias(request, id_caso):
    caso =  Caso.objects.get(id = id_caso)
    concurrencias = Concurrencia.objects.filter(caso = caso)
    template_path = 'casos/descargar_pdf_concurrencias.html'
    template = get_template(template_path)
    context = {
        'concurrencias': concurrencias,
        'caso' : caso
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "Concurrencias.pdf"'  # si comento esta linea el pdf aparece en el navegador en vez de descargarse
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def operador_busqueda(request):
    if request.user.is_staff :
        if (request.method == 'POST'):
            searched = request.POST['searched'].strip()
            nombre_buscado = ' '
            apellido_buscado = ' '
            if ' ' in searched :
                nombre_buscado, apellido_buscado = searched.split()
            else:
                nombre_buscado = searched
                apellido_buscado = searched
            victimas = Victima.objects.filter(Q(nombre__contains = nombre_buscado) | Q(apellido__contains = apellido_buscado) | Q(documento__contains = searched))
            context = {
                "victimas": victimas,
            }
            return render(request, "casos/operador_busqueda.html", context=context)
        else:
            return render(request, "casos/operador_busqueda.html", context={})
    else:
        response = redirect('/')
        return response
        
@login_required
def operador_resultado(request, id_victima):
    if request.user.is_staff :
        victima = Victima.objects.get(id = id_victima)
        context = {
            "victima": victima,
            "casos": Caso.objects.filter(victima = victima),
            "contactos": Contacto.objects.filter(victima = victima),
        }
        return render(request, "casos/operador_resultado.html", context=context)
    else:
        response = redirect('/')
        return response

@login_required
def operador_ver_caso(request, id_caso):
    if request.user.is_staff :
        caso = Caso.objects.get(id = id_caso)
        agresores = caso.agresor.all()
        concurrencias = Concurrencia.objects.filter(caso = caso)
        incidencias = Incidencia.objects.filter(caso = caso)
        documentos = Documento.objects.filter(caso = caso) 
        context = {
            "caso": caso, 
            "incidencias" : incidencias,
            "concurrencias" : concurrencias,
            "documentos" : documentos, 
            "agresores": agresores
        }
        return render(request, "casos/operador_ver_caso.html", context=context)
    else:
        response = redirect('/')
        return response

@login_required
def operador_concurrencia(request, id_caso):
    if request.user.is_staff :
        caso = Caso.objects.get(id = id_caso)
        if caso.estado == "ABIERTO":
            concurrencia = Concurrencia(caso = caso, lugar_concurrido ='', descripcion='')
            form_concurrencia = ConcurrenciaForm(request.POST or None, request.FILES or None, instance=concurrencia)
            context = {
                "caso": caso,
                "form_concurrencia" : form_concurrencia,
            }
            if form_concurrencia.is_valid():
                form_concurrencia.save()
                response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
                return response
            return render(request, "casos/operador_concurrencia.html", context = context)
        else:
            context = {
                "caso": caso,
            }
            messages.info(request, 'La causa que intentas actualizar esta cerrada')
            response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
            return response
    else:
        response = redirect('/')
        return response

@login_required
def agregar_incidencia(request, id_caso):
    if request.user.is_staff :
        caso = Caso.objects.get(id = id_caso)
        if caso.estado == "ABIERTO":
            incidencia = Incidencia(caso = caso, fecha ='', descripcion='', nombre='')
            form_incidencia = IncidenciaForm(request.POST or None, request.FILES or None, instance=incidencia)
            context = {
                "caso": caso,
                "form_incidencia" : form_incidencia,
            }
            if form_incidencia.is_valid():
                form_incidencia.save()
                response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
                return response
            return render(request, "casos/agregar_incidencia.html", context = context)
        else:
            context = {
                "caso": caso,
            }
            messages.info(request, 'La causa que intentas actualizar esta cerrada')
            response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
            return response

    else:
        response = redirect('/')
        return response

@login_required
def agregar_documento(request,id_caso):
    if request.user.is_staff :
        caso = Caso.objects.get(id = id_caso)
        if caso.estado == "ABIERTO":
            documento = Documento(caso = caso, archivo ='', descripcion='', fecha ='', mimetype='')
            form_documento = DocumentoForm(request.POST or None, request.FILES or None, instance=documento, caso=caso)
            context = {
                "caso": caso,
                "form_documento" : form_documento,
            }
            if form_documento.is_valid():
                form_documento.save()
                response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
                return response
            return render(request, "casos/agregar_documento.html", context = context)
        else:
            context = {
                "caso": caso,
            }
            messages.info(request, 'La causa que intentas actualizar esta cerrada')
            response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
            return response
    else:
        response = redirect('/')
        return response

@login_required
def operador_editar_agresor(request, id_caso, id_agresor):
    if request.user.is_staff :
        caso = Caso.objects.get(id = id_caso)
        agresor = Agresor.objects.get(id = id_agresor)
        domicilio = agresor.domicilio
        form_agresor = AgresorCasoForm(request.POST or None, request.FILES or None, instance=caso)
        form_domicilio = DomicilioForm(request.POST or None, request.FILES or None, instance=domicilio)
        form_agresor_caso = AgresorForm(request.POST or None, request.FILES or None, instance=agresor)
        context = {
            "form_agresor" : form_agresor,
            "form_agresor_caso" : form_agresor_caso,
            "form_domicilio" : form_domicilio,
            "caso_id" : id_caso,
        }
        if form_agresor.is_valid() and form_domicilio.is_valid() and form_agresor_caso.is_valid():
            form_agresor.save()
            form_domicilio.save()
            response = redirect('/operador_resultado/operador_ver_caso/'+id_caso)
            return response
        return render(request, "casos/operador_editar_agresor.html", context = context)
    else:
        response = redirect('/')
        return response
    
