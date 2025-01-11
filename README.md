# Late Apply

## Description
Proyecto minimo para administrar agilmente las inscripciones tardías de la carrera de Ingeniería en Sistemas

## Prerequisites
- Python 3.x
- Django
- pip (Python package installer)

## Model

- **Alumno**: Representa a un estudiante con un legajo único, nombre y apellido.
- **Materia**: Representa una materia que puede tener varios cursos asociados.
- **Curso**: Representa un curso único de una materia específica y una comisión, en un año y cuatrimestre en particular.
- **InscripcionTardia**: Representa la inscripción tardía de un alumno a una materia, con preferencias de comisiones.
- **Cursado**: El cursado de un alumno en un curso en particular, registrando su estado para futuro analisis.

### Relaciones entre modelos:
- Un **Alumno** puede tener múltiples **InscripcionTardia**.
- Una **Materia** puede tener múltiples **Curso**.
- Un **Curso** pertenece a una **Materia**.
- Un **Curso** puede tener múltiples **Cursado**.
- Un **Alumno** puede tener múltiples **Cursado**.
- Una **InscripcionTardia** pertenece a un **Alumno** y a una **Materia**.

## Database Migration
Para migrar la base de datos, ejecutar estos comandos

1. Make migrations:
    ```sh
    python manage.py makemigrations
    ```

2. Apply migrations:
    ```sh
    python manage.py migrate
    ```

## Running the Project
Para levantar la aplicación ejecutar el siguiente comando
```sh
python manage.py runserver
```

### URLS
- http://localhost:8000/admin/
- http://localhost:8000/swagger/

### Endpoints
- http://localhost:8000/api/inscripciones
- http://localhost:8000/api/cursos

## License
Libre de uso xq somos cool UwU