from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Curso, InscripcionTardia, Alumno, Materia, Comision
from django.db import transaction
from .utils.greedy_algorithm import greedy_assignment, optimize_assignments, Assignable, Containable
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import AlumnoSerializer
from drf_yasg.utils import swagger_auto_schema

# List and Create (GET and POST)
class AlumnoListCreateView(ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

# Retrieve, Update, and Delete (GET, PUT, PATCH, DELETE)
class AlumnoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer





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

                    # Ensure Comision exists, create if not
                    comision, comision_created = Comision.objects.get_or_create(codigo=comision_code)

                    # Create Curso
                    curso = Curso.objects.create(
                        materia=materia,
                        comision=comision,
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

                    nombre = record.get("Nombre")
                    apellido = record.get("Apellido")
                    legajo = record.get("Confirmar Legajo")
                    materia_name = record.get("Materia")
                    comision1_code = record.get("Comisión (Opción 1)")
                    comision2_code = record.get("Comisión Opción 2")

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

                    # Ensure Comisiones exist
                    try:
                        comision1 = Comision.objects.get(codigo=comision1_code)
                        comision2 = Comision.objects.get(codigo=comision2_code)
                    except Comision.DoesNotExist:
                        return Response({"error": "One or both Comisiones not found"}, status=status.HTTP_400_BAD_REQUEST)

                    # Get or create Alumno
                    alumno, created = Alumno.objects.get_or_create(
                        legajo=legajo,
                        defaults={"nombre": nombre, "apellido": apellido}  
                    )

                    # Create InscripcionTardia
                    inscripcion = InscripcionTardia.objects.create(
                        alumno=alumno,
                        materia=materia,
                        comision1=comision1,
                        comision2=comision2,
                    )
                    created_records.append(inscripcion.id)
            
            return Response(
                {"message": "Inscripciones created", "created_ids": created_records},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
                preferences=[inscripcion.comision1.id, inscripcion.comision2.id]
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
                    "curso": f"{materia.nombre} - {curso.comision.codigo}",
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




# No se si dejar esto o no
class InscripcionTardiaAssignmentView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Endpoint to fetch Inscripciones Tardias and Cursos from the database,
        apply the greedy algorithm based on comision1 and comision2 preferences, 
        and return the assignment results.
        """
        # Fetch InscripcionTardias and Cursos from the database
        inscripciones_tardias = InscripcionTardia.objects.all()
        cursos = Curso.objects.all()

        # Create Assignable and Containable instances for the greedy algorithm
        assignables = [
            Assignable(inscripcion.id, [inscripcion.comision1.id, inscripcion.comision2.id])
            for inscripcion in inscripciones_tardias
        ]
        
        containables = [
            Containable(curso.id, curso.cupo - curso.inscriptos)  # Capacity of cursos
            for curso in cursos
        ]

        # Build the JSON structure
        result = []
        for materia in materias:
            materia_data = {
                "materia": materia.nombre,
                "cursos": []
            }
            for curso in materia.curso_set.all():
                curso_data = {
                    "curso": curso.comision.codigo,
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

        # First pass using greedy algorithm
        unplaced_assignables, updated_containables = greedy_assignment(assignables, containables)

        # Optionally optimize the assignment
        final_unplaced_assignables, final_containables = optimize_assignments(unplaced_assignables, updated_containables)

        # Prepare response data
        result = {
            "assigned": [{"inscripcion_id": assignable.id, "curso_id": containable.id} for containable in final_containables for assignable in containable.objects],
            "unassigned": [assignable.id for assignable in final_unplaced_assignables]
        }

        # Optionally update the database with the assigned Inscripciones (if needed)
        for containable in final_containables:
            curso = Curso.objects.get(id=containable.id)
            for obj in containable.objects:
                inscripcion = InscripcionTardia.objects.get(id=obj.id)
                inscripcion.curso = curso
                inscripcion.save()

        return Response(result, status=status.HTTP_200_OK)


class DistributeAlumnosView(APIView):
    @swagger_auto_schema(operation_description="Distribute alumnos among cursos")
    def get(self, request, materia_id):
        try:
            materia = Materia.objects.get(id=materia_id)
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