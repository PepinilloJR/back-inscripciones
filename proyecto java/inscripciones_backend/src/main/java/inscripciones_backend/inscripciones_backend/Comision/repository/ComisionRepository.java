package inscripciones_backend.inscripciones_backend.Comision.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Comision.models.Comision;

@Repository
public interface ComisionRepository extends JpaRepository<Comision,Long>{

    @Query("SELECT c FROM Comision c WHERE c.codigo = :codigo")
    Optional<Comision> findByCodigo(@Param("codigo") String codigo);
}
