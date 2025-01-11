from django.core.management.base import BaseCommand
from lateapp.models import Alumno, Materia, Curso, InscripcionTardia, Cursado

class Command(BaseCommand):
    help = 'Populate the database with hardcoded data'

    def handle(self, *args, **kwargs):
        # Hardcoded data for Alumno
        alumnos_data = [
            {'legajo': 1001, 'nombre': 'Juan', 'apellido': 'Perez'},
            {'legajo': 1002, 'nombre': 'Maria', 'apellido': 'Gomez'},
            {'legajo': 1003, 'nombre': 'Carlos', 'apellido': 'Lopez'},
            {'legajo': 1004, 'nombre': 'Ana', 'apellido': 'Martinez'},
            {'legajo': 1005, 'nombre': 'Luis', 'apellido': 'Garcia'},
        ]

        # Hardcoded data for Materia
        materias_data = [
            {'nombre': 'Analisis Matematico 2'},
            {'nombre': 'Ingenieria y Sociedad'},
            {'nombre': 'Sistemas de Gestion'},
            {'nombre': 'Algoritmos y Estructuras de Datos'},
            {'nombre': 'Arquitectura de Computadoras'},
        ]

        # Create Alumno instances
        for alumno_data in alumnos_data:
            Alumno.objects.create(**alumno_data)

        # Create Materia instances
        for materia_data in materias_data:
            Materia.objects.create(**materia_data)

        # Hardcoded data for Curso
        cursos_data = [
            {'materia': Materia.objects.get(nombre='Analisis Matematico 2'), 'comision': '2K2', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 8, 'hora_fin': 10, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Analisis Matematico 2'), 'comision': '2K3', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 10, 'hora_fin': 12, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Ingenieria y Sociedad'), 'comision': '3K2', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 10, 'hora_fin': 12, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Ingenieria y Sociedad'), 'comision': '3K3', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 12, 'hora_fin': 14, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Sistemas de Gestion'), 'comision': '4K4', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 12, 'hora_fin': 14, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Sistemas de Gestion'), 'comision': '4K5', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 14, 'hora_fin': 16, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Algoritmos y Estructuras de Datos'), 'comision': '1K8', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 14, 'hora_fin': 16, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Algoritmos y Estructuras de Datos'), 'comision': '1K7', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 16, 'hora_fin': 18, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Arquitectura de Computadoras'), 'comision': '2K3', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 16, 'hora_fin': 18, 'cupo': 30},
            {'materia': Materia.objects.get(nombre='Arquitectura de Computadoras'), 'comision': '2K4', 'year': 2025, 'cuatrimestre': 'Primero', 'hora_inicio': 18, 'hora_fin': 20, 'cupo': 30},
        ]

        # Create Curso instances
        for curso_data in cursos_data:
            Curso.objects.create(**curso_data)

        # Hardcoded data for InscripcionTardia
        inscripciones_data = [
            {'alumno': Alumno.objects.get(legajo=1001), 'materia': Materia.objects.get(nombre='Analisis Matematico 2'), 'comision1': '2K2', 'comision2': '2K3'},
            {'alumno': Alumno.objects.get(legajo=1002), 'materia': Materia.objects.get(nombre='Ingenieria y Sociedad'), 'comision1': '3K2', 'comision2': '3K3'},
            {'alumno': Alumno.objects.get(legajo=1003), 'materia': Materia.objects.get(nombre='Sistemas de Gestion'), 'comision1': '4K4', 'comision2': '4K5'},
            {'alumno': Alumno.objects.get(legajo=1004), 'materia': Materia.objects.get(nombre='Algoritmos y Estructuras de Datos'), 'comision1': '1K8', 'comision2': '1K7'},
            {'alumno': Alumno.objects.get(legajo=1005), 'materia': Materia.objects.get(nombre='Arquitectura de Computadoras'), 'comision1': '2K3', 'comision2': '2K4'},
        ]

        # Create InscripcionTardia instances
        for inscripcion_data in inscripciones_data:
            InscripcionTardia.objects.create(**inscripcion_data)

        # Hardcoded data for Cursado
        cursados_data = [
            {'alumno': Alumno.objects.get(legajo=1001), 'curso': Curso.objects.get(comision='2K2', materia=Materia.objects.get(nombre='Analisis Matematico 2'))},
            {'alumno': Alumno.objects.get(legajo=1002), 'curso': Curso.objects.get(comision='3K2', materia=Materia.objects.get(nombre='Ingenieria y Sociedad'))},
            {'alumno': Alumno.objects.get(legajo=1003), 'curso': Curso.objects.get(comision='4K4', materia=Materia.objects.get(nombre='Sistemas de Gestion'))},
            {'alumno': Alumno.objects.get(legajo=1004), 'curso': Curso.objects.get(comision='1K8', materia=Materia.objects.get(nombre='Algoritmos y Estructuras de Datos'))},
            {'alumno': Alumno.objects.get(legajo=1005), 'curso': Curso.objects.get(comision='2K3', materia=Materia.objects.get(nombre='Arquitectura de Computadoras'))},
        ]

        # Create Cursado instances
        for cursado_data in cursados_data:
            Cursado.objects.create(**cursado_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with hardcoded data'))