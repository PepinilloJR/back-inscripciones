from django.db import models
from django.forms import ValidationError


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

    def distribute_alumnos(self):
        # Step 1: Fetch Cursos for this Materia
        cursos = list(self.cursos.all())

        # Step 2: Fetch InscripcionesTardias for this Materia
        inscripciones = InscripcionTardia.objects.filter(materia=self)

        # Step 3: Prepare distribution data structures
        distribution = {curso: [] for curso in cursos}  # Map Cursos to their Alumnos
        unasigned = []  # Alumnos that could not be assigned

        # Step 4: Implement the distribution algorithm
        for inscripcion in inscripciones:
            # Attempt to place in preferred Curso
            preferred_curso = next((curso for curso in cursos if curso.comision == inscripcion.comision1), None)
            secondary_curso = next((curso for curso in cursos if curso.comision == inscripcion.comision2), None)

            # Place Alumno in the preferred Curso if it has space
            if preferred_curso and preferred_curso.inscriptos < preferred_curso.cupo:
                distribution[preferred_curso].append(inscripcion.alumno)
                preferred_curso.inscriptos += 1
            # Otherwise, place in the secondary Curso
            elif secondary_curso and secondary_curso.inscriptos < secondary_curso.cupo:
                distribution[secondary_curso].append(inscripcion.alumno)
                secondary_curso.inscriptos += 1
            # If neither has space, add to unassigned list
            else:
                unasigned.append(inscripcion.alumno)
            

        # Step 5: Return the distribution and unassigned Alumnos
        return distribution, unasigned
    
    def optimize_distribution(self):
        # Step 1: Perform the initial distribution
        distribution, unassigned = self.distribute_alumnos()

        # Rearrange items to make room
        for curso in self.cursos.all():
            if curso.inscriptos == curso.cupo:  # If the course is full
                for alumno in list(distribution[curso]):  # Loop over the alumnos in the curso
                    if curso.inscriptos < curso.cupo:  
                        break  # Stop once the container is no longer full
                    
                    inscripcion = InscripcionTardia.objects.filter(alumno=alumno, materia=self).last()
                    if inscripcion:
                        # Try to move the alumno to their secondary preferred curso
                        secondary_curso = next((c for c in self.cursos.all() if c.comision == inscripcion.comision2), None)
                        # If the secondary curso has space, move the alumno
                        if secondary_curso and secondary_curso.inscriptos < secondary_curso.cupo:
                            distribution[curso].remove(alumno)
                            distribution[secondary_curso].append(alumno)
                            secondary_curso.inscriptos += 1
                            curso.inscriptos -= 1
                            break # Stop once the container is no longer full

        # Step 3: After rearranging, try placing the remaining unassigned alumnos
        for alumno in unassigned:
            placed = False
            inscripcion = InscripcionTardia.objects.filter(alumno=alumno, materia=self).first()
            if inscripcion:
                preferred_curso = next((curso for curso in self.cursos.all() if curso.comision == inscripcion.comision1), None)
                if preferred_curso and preferred_curso.inscriptos < preferred_curso.cupo:
                    # Place the alumno in their preferred curso
                    distribution[preferred_curso].append(alumno)
                    preferred_curso.inscriptos += 1
                    unassigned.remove(alumno)
                    placed = True

                # If the alumno still couldn't be placed, try their secondary preferred curso
                if not placed:
                    secondary_curso = next((curso for curso in self.cursos.all() if curso.comision == inscripcion.comision2), None)
                    if secondary_curso and secondary_curso.inscriptos < secondary_curso.cupo:
                        # Place the alumno in their secondary preferred curso
                        distribution[secondary_curso].append(alumno)
                        secondary_curso.inscriptos += 1
                        unassigned.remove(alumno)

        # Step 4: Return the optimized distribution and unassigned alumnos
        return distribution, unassigned


    
    

class Curso(models.Model):
    # Nombre de la materia y comision
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    comision = models.CharField(max_length=5)  # Changed to CharField

    # Cuatrimetres en los que se dicta el curso y horario de inicio y fin
    year = models.IntegerField(default=2025)
    cuatrimestre = models.CharField(max_length=20)
    hora_inicio = models.IntegerField()
    hora_fin = models.IntegerField()

    # Cantidad de cupos disponibles, cantidad de inscriptos
    cupo = models.IntegerField()
    inscriptos = models.IntegerField(default=0)

    # Constraint que evita duplicados de materia y comision
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['materia', 'comision', 'year', 'cuatrimestre'], name='unique_mat_com_year_cuat')
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
    comision1 = models.CharField(max_length=5)  # Changed to CharField
    # Comision secundaria a la que se inscribe
    comision2 = models.CharField(max_length=5)  # Changed to CharField
    
    def __str__(self):
        return f"{self.alumno.legajo} - {self.comision1} - {self.comision2}"
    

# Alumno x Curso
class Cursado(models.Model):
    # Alumno que cursa
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    # Curso que cursa
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    # Estado de cursado
    estado = models.CharField(max_length=20, default='Inscripto')
    
    # Save modification that checks there is space in the Curso before saving
    def save(self, *args, **kwargs):
        # Check if the curso has available spots
        if self.curso.inscriptos >= self.curso.cupo:
            raise ValidationError('No hay cupos disponibles para este curso.')
        else:
            # Increment the inscriptos count
            self.curso.inscriptos += 1
            self.curso.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno.legajo} - {self.curso}"
