from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="casos-home"),
    path("perfil/", views.perfil, name="casos-perfil"),
    path("perfil/caso/<id>", views.caso, name="casos-caso"),
    path("editar_perfil/", views.editar_perfil, name="casos-editar_perfil"),
    path("agregar_contacto/", views.agregar_contacto, name="casos-agregar_contacto"),
    path("perfil/caso/documentos/<id_caso>/<id_doc>", views.documentos, name="casos-documentos"),
    path("editar_contacto/<id_contacto>", views.editar_contacto, name="casos-editar_contacto"),
    path("descargar/<id_doc>", views.descargar, name="descargar"),
    path("operador_busqueda/", views.operador_busqueda, name="casos-operador_busqueda"),
    path("operador_resultado/<id_victima>", views.operador_resultado, name="casos-operador_resultado"),
    path("operador_resultado/operador_ver_caso/<id_caso>", views.operador_ver_caso, name="casos-operador_ver_caso"),
    path("operador_editar_agresor/<id_caso>/<id_agresor>", views.operador_editar_agresor, name="casos-operador_editar_agresor"),
    path("operador_concurrencia/<id_caso>", views.operador_concurrencia, name="casos-operador_concurrencia"),
    path("agregar_incidencia/<id_caso>", views.agregar_incidencia, name="casos-agregar_incidencia"),
    path("agregar_documento/<id_caso>", views.agregar_documento, name="casos-agregar_documento"),
    path("descargar_concurrencias/<id_caso>", views.descargar_pdf_concurrencias, name="casos-descargar_pdf_concurrencias"),
    path("operador_descargar_manual/", views.operador_descargar_manual, name = "casos-operador_descargar_manual"),
]
