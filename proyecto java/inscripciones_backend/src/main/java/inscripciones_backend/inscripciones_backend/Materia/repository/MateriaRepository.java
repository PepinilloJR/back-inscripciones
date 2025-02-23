package inscripciones_backend.inscripciones_backend.Materia.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import inscripciones_backend.inscripciones_backend.Materia.model.Materia;

@Repository
public interface MateriaRepository extends JpaRepository<Materia,Long> {
    @Query("SELECT m FROM Materia m WHERE m.nombre = :nombre")
    Optional<Materia> findByNombre(@Param("nombre") String nombre);
}
