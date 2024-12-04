from django.contrib import admin

from lateapp.models import Alumno, Comision, Curso, InscripcionTardia, Materia

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(Comision)
admin.site.register(InscripcionTardia)
admin.site.register(Curso)
