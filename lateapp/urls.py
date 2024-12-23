from django.urls import path, re_path

from . import views


urlpatterns = [
    # Crud
    path('alumnos/', views.AlumnoListCreateView.as_view(), name='alumno-list-create'),
    path('alumnos/<int:pk>/', views.AlumnoDetailView.as_view(), name='alumno-detail'),

    path("inscripciones/bulk", views.InscripcionTardiaBulkCreateView.as_view(), name="bulk_create_inscripciones"),
    path("cursos/bulk", views.CursoBulkCreateView.as_view(), name="bulk_create_cursos"),

    path("cursos/", views.CursoListCreateView.as_view(), name="curso-list-create"),
    path("cursos/<int:pk>/", views.CursoDetailView.as_view(), name="curso-detail"),

    path("cursados/", views.CursadoListCreateView.as_view(), name="cursado-list-create"),
    path("cursados/<int:pk>/", views.CursadoDetailView.as_view(), name="cursado-detail"),

    path('materias/', views.MateriaListCreateView.as_view(), name='materia-list-create'),
    path('materias/<int:pk>/', views.MateriaDetailView.as_view(), name='materia-detail'),
    path('materias/inscripciones/<int:materia_nombre>/', views.InscripcionesPorMateriaView.as_view(), name='inscripciones_por_materia'),

    path('materia/distribute/<int:materia_nombre>/', views.DistributeAlumnosView.as_view(), name='distribute_alumnos'),
    path('materia/optimize/<int:materia_nombre>/', views.OptimizeDistributionView.as_view(), name='optimize_distribution'),
]