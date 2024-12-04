from django.urls import path, re_path

from . import views


urlpatterns = [
    # Crud
    path('alumnos/', views.AlumnoListCreateView.as_view(), name='alumno-list-create'),
    path('alumnos/<int:pk>/', views.AlumnoDetailView.as_view(), name='alumno-detail'),

    path("inscripciones/", views.InscripcionTardiaBulkCreateView.as_view(), name="bulk_create_inscripciones"),
    path("cursos/", views.CursoBulkCreateView.as_view(), name="bulk_create_cursos"),

    path('materia/distribute/<int:materia_id>/', views.DistributeAlumnosView.as_view(), name='distribute_alumnos'),
    path('materia/optimize/<int:materia_id>/', views.OptimizeDistributionView.as_view(), name='optimize_distribution'),
]