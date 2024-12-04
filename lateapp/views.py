from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Curso, InscripcionTardia, Alumno, Materia, Comision
from django.db import transaction

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
        data = request.data  # List of inscripciones
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
