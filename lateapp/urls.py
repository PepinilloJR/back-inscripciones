from django.urls import path, re_path

from . import views



urlpatterns = [

    path("api/inscripciones/", views.InscripcionTardiaBulkCreateView.as_view(), name="bulk_create_inscripciones"),
    path("api/cursos/", views.CursoBulkCreateView.as_view(), name="bulk_create_cursos"),
]