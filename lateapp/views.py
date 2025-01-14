from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Curso, InscripcionTardia, Alumno, Materia
from django.db import transaction
from .utils.greedy_algorithm import greedy_assignment, optimize_assignments, Assignable, Containable
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from drf_yasg.utils import swagger_auto_schema

# ------------------------------------------- CRUD views -------------------------------------------
# List and Create (GET and POST)
class AlumnoListCreateView(ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
# Retrieve, Update, and Delete (GET, PUT, PATCH, DELETE)
class AlumnoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class MateriaListCreateView(ListCreateAPIView):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
class MateriaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class CursoListCreateView(ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
class CursoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CursadoListCreateView(ListCreateAPIView):
    queryset = Cursado.objects.all()
    serializer_class = CursadoSerializer
class CursadoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Cursado.objects.all()
    serializer_class = CursadoSerializer

class InscripcionTardiaListCreateView(ListCreateAPIView):
    queryset = InscripcionTardia.objects.all()
    serializer_class = InscripcionTardiaSerializer
class InscripcionTardiaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = InscripcionTardia.objects.all()
    serializer_class = InscripcionTardiaSerializer

# ------------------------------------------- CRUD views -------------------------------------------

# ------------------------------------------- Bulk views -------------------------------------------
class CursoBulkCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # List of Cursos in the provided JSON
        created_records = []
        
        try:
            with transaction.atomic():  # Ensure all-or-nothing behavior
                for record in data:
                    materia_name = record.get("materia")
                    comision_code = record.get("comision")
                    cuatrimestre = record.get("diccomisio")
                    hora_inicio = record.get("hd")
                    hora_fin = record.get("hh")
                    inscriptos = record.get("inscriptos")
                    cupo = record.get("cupo")

                    if not all([materia_name, comision_code, cuatrimestre, hora_inicio, hora_fin, inscriptos is not None]):
                        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

                    # Ensure Materia exists, create if not
                    materia, materia_created = Materia.objects.get_or_create(nombre=materia_name)

                    # Create Curso
                    curso = Curso.objects.create(
                        materia=materia,
                        comision=comision_code,  # Changed to use comision_code directly
                        cuatrimestre=cuatrimestre,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                        cupo=cupo,
                        inscriptos=inscriptos
                    )
                    created_records.append(curso.id)
            
            return Response(
                {"message": "Cursos created", "created_ids": created_records},
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InscripcionTardiaBulkCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # List of inscripciones in the provided JSON
        created_records = []

        # Print the incoming data to debug
        print("Received data:", data)

        # Clean the keys (remove spaces from field names)
        cleaned_data = []
        for record in data:
            cleaned_record = {key.strip(): value for key, value in record.items()}
            cleaned_data.append(cleaned_record)
        
        try:
            with transaction.atomic():  # Ensure all-or-nothing behavior
                for record in cleaned_data:
                    # Debug the cleaned data for each record
                    print("Processing record:", record)

                    nombre = record.get("nombre")
                    apellido = record.get("apellido")
                    legajo = record.get("legajo")
                    materia_name = record.get("materia")
                    comision1_code = record.get("comision1")
                    comision2_code = record.get("comision2")

                    # Print field values to verify
                    print("Nombre:", nombre)
                    print("Apellido:", apellido)
                    print("Legajo:", legajo)
                    print("Materia:", materia_name)
                    print("Comisión (Opción 1):", comision1_code)
                    print("Comisión Opción 2:", comision2_code)

                    # Check for missing fields
                    if not all([apellido, legajo, materia_name, comision1_code, comision2_code]):
                        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

                    # Ensure Materia exists
                    try:
                        materia = Materia.objects.get(nombre=materia_name)
                    except Materia.DoesNotExist:
                        return Response({"error": f"Materia '{materia_name}' not found"}, status=status.HTTP_400_BAD_REQUEST)

                    # Get or create Alumno
                    alumno, created = Alumno.objects.get_or_create(
                        legajo=legajo,
                        defaults={"nombre": nombre, "apellido": apellido}  
                    )

                    # Create InscripcionTardia
                    inscripcion = InscripcionTardia.objects.create(
                        alumno=alumno,
                        materia=materia,
                        comision1=comision1_code,  # Changed to use comision1_code directly
                        comision2=comision2_code,  # Changed to use comision2_code directly
                    )
                    created_records.append(inscripcion.id)
            
            return Response(
                {"message": "Inscripciones created", "created_ids": created_records},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ------------------------------------------- Bulk views -------------------------------------------


class MateriaCursosView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch all data from the database
        materias = Materia.objects.prefetch_related("curso_set", "curso_set__inscripciontardia_set")
        cursos = Curso.objects.prefetch_related("inscripciontardia_set")
        inscripciones = InscripcionTardia.objects.select_related("alumno", "curso")

        # Prepare data for greedy algorithm
        assignables = [
            Assignable(
                id=inscripcion.id,
                preferences=[inscripcion.comision1, inscripcion.comision2]  # Changed to use comision1 and comision2 directly
            )
            for inscripcion in inscripciones
        ]
        containables = [
            Containable(
            id=curso.id,
            capacity=curso.cupo - curso.inscriptos
            )
            for curso in cursos
        ]

        # Sort InscripcionesTardias into Cursos
        unplaced, sorted_cursos = greedy_assignment(assignables, containables)

        # Build the JSON structure
        result = []
        for materia in materias:
            materia_data = {
                "materia": materia.nombre,
                "cursos": []
            }
            for curso in materia.curso_set.all():
                curso_data = {
                    "curso": f"{materia.nombre} - {curso.comision}",  # Changed to use comision directly
                    "inscripciones": [
                        {
                            "alumno": f"{inscripcion.alumno.nombre} {inscripcion.alumno.apellido}",
                            "legajo": inscripcion.alumno.legajo
                        }
                        for inscripcion in curso.inscripciontardia_set.all()
                    ]
                }
                materia_data["cursos"].append(curso_data)
            result.append(materia_data)

        # Return the JSON response
        return Response(result, status=200)



class InscripcionesPorMateriaView(APIView):
    def get(self, request, materia_nombre):
        try:
            materia = Materia.objects.get(nombre=materia_nombre)
            inscripcionesTardias = InscripcionTardia.objects.filter(materia=materia)
            data = {
                "materia": materia.nombre,
                "alumnos": [{
                    "legajo": inscripcionTardia.alumno.legajo,
                    "nombre": inscripcionTardia.alumno.nombre,
                    "apellido": inscripcionTardia.alumno.apellido,
                    "Comision 1": inscripcionTardia.comision1,
                    "Comision 2": inscripcionTardia.comision2
                    } for inscripcionTardia in inscripcionesTardias]
            }
            return JsonResponse(data, status=200)
        except Materia.DoesNotExist:
            return JsonResponse({"error": "Materia not found"}, status=404)


class DistributeAlumnosView(APIView):
    @swagger_auto_schema(operation_description="Distribute alumnos among cursos")
    def get(self, request, materia_nombre):
        try:
            materia = Materia.objects.get(nombre=materia_nombre)
            distribution, unassigned = materia.distribute_alumnos()

            # Prepare the response data
            distribution_data = {
                "distribution": {
                    str(curso.id): [alumno.legajo for alumno in alumnos] 
                    for curso, alumnos in distribution.items()
                },
                "unassigned": [alumno.legajo for alumno in unassigned]
            }

            return JsonResponse(distribution_data, status=200)

        except Materia.DoesNotExist:
            return JsonResponse({"error": "Materia not found"}, status=404)
        

class OptimizeDistributionView(APIView):
    @swagger_auto_schema(operation_description="Optimize alumnos distribution")
    def get(self, request, materia_id):
        try:
            materia = Materia.objects.get(id=materia_id)
            distribution, unassigned = materia.optimize_distribution()

            # Prepare the response data
            distribution_data = {
                "distribution": {
                    str(curso.id): [alumno.id for alumno in alumnos]
                    for curso, alumnos in distribution.items()
                },
                "unassigned": [alumno.legajo for alumno in unassigned]
            }

            return JsonResponse(distribution_data, status=200)

        except Materia.DoesNotExist:
            return JsonResponse({"error": "Materia not found"}, status=404)
