from django.db import models


class Alumno(models.Model):
    legajo = models.IntegerField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Comision(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.codigo
    
class Curso(models.Model):
    # Nombre de la materia y comision
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)

    # Cuatrimetres en los que se dicta el curso y horario de inicio y fin
    cuatrimestre = models.CharField(max_length=20)
    hora_inicio = models.IntegerField()
    hora_fin = models.IntegerField()

    # Cantidad de cupos disponibles, cantidad de inscriptos
    cupo = models.IntegerField()
    inscriptos = models.IntegerField(default=0)


    # Constraint que evita duplicados de materia y comision
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['materia', 'comision'], name='unique_materia_comision')
        ]
    
    # Metodo que devuelve el nombre y comision del curso
    def __str__(self):
        return f"{self.materia.nombre} - {self.comision}"



class InscripcionTardia(models.Model):
    # Alumno que se inscribe
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    
    # Materia a la que se inscribe
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    # Comision preferida a la que se inscribe
    comision1 = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='inscripcion_preferida')
    # Comision secundaria a la que se inscribe
    comision2 = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='inscripcion_secundaria')

    def __str__(self):
        return self.alumno.nombre + " inscripto en " + self.materia.nombre