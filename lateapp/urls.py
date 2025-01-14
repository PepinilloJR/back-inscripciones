from django.urls import path, re_path

from . import views


urlpatterns = [
    # Crud
    path('alumnos/', views.AlumnoListCreateView.as_view(), name='alumno-list-create'),
    path('alumnos/<int:pk>/', views.AlumnoDetailView.as_view(), name='alumno-detail'),

    path("inscripciones/", views.InscripcionTardiaListCreateView.as_view(), name="inscripcion-list-create"),
    path("inscripciones/<int:pk>/", views.InscripcionTardiaDetailView.as_view(), name="inscripcion-detail"),
    path("inscripciones/bulk", views.InscripcionTardiaBulkCreateView.as_view(), name="bulk_create_inscripciones"),

    # Inscripciones por materia, algoritmo de distribución y algoritmo de optimización
    path('inscripciones/materia/<int:materia_id/', views.InscripcionesPorMateriaView.as_view(), name='inscripciones_por_materia'),
    path('inscripciones/materia/distribute/<int:materia_id>/', views.DistributeAlumnosView.as_view(), name='distribute_alumnos'),
    path('inscripciones/materia/optimize/<int:materia_id>/', views.OptimizeDistributionView.as_view(), name='optimize_distribution'),


    path("cursos/", views.CursoListCreateView.as_view(), name="curso-list-create"),
    path("cursos/<int:pk>/", views.CursoDetailView.as_view(), name="curso-detail"),
    path("cursos/bulk", views.CursoBulkCreateView.as_view(), name="bulk_create_cursos"),

    path("cursados/", views.CursadoListCreateView.as_view(), name="cursado-list-create"),
    path("cursados/<int:pk>/", views.CursadoDetailView.as_view(), name="cursado-detail"),

    path('materias/', views.MateriaListCreateView.as_view(), name='materia-list-create'),
    path('materias/<int:pk>/', views.MateriaDetailView.as_view(), name='materia-detail'),


]