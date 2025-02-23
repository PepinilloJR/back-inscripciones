# Proyecto Back-inscripciones

Este es un proyecto basado en Spring Boot que proporciona el backend para la inscripcion tardia de estudiantes.

## Requisitos previos

Antes de ejecutar este proyecto, asegúrate de tener instalados los siguientes requisitos:

- version de Java 23+
- Maven 3.x
- Base de datos MySql

### Construcción y ejecución con Maven
```sh
 mvn clean install
 mvn spring-boot:run
```
## Configuración

Este proyecto utiliza un archivo de configuración en `application.properties`. Modifica las propiedades necesarias antes de ejecutar el proyecto.

Ejemplo (`src/main/resources/application.properties`):
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/mi_base
spring.datasource.username=usuario
spring.datasource.password=contraseña
```
