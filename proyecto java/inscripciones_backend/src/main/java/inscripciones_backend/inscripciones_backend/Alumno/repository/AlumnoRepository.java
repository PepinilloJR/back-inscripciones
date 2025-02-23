package inscripciones_backend.inscripciones_backend.Alumno.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;

@Repository
public interface AlumnoRepository extends JpaRepository<Alumno,Long> {
    @Query("SELECT a FROM Alumno a WHERE a.nombre = :nombre AND a.apellido = :apellido")
    Optional<Alumno> findByNombreApellido(@Param("nombre") String nombre, @Param("apellido") String apellido);
}
