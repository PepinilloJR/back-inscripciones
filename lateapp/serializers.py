from rest_framework import serializers

from lateapp.models import Alumno, Curso, Materia

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    alumnos = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = ['comision', 'cuatrimestre', 'hora_inicio', 'hora_fin', 'cupo', 'inscriptos', 'alumnos']

    def get_alumnos(self, obj):
        return obj.get_alumnos()  # Call the method to get the list of Alumnos

class MateriaSerializer(serializers.ModelSerializer):
    cursos = CursoSerializer(many=True)

    class Meta:
        model = Materia
        fields = ['nombre', 'cursos']



