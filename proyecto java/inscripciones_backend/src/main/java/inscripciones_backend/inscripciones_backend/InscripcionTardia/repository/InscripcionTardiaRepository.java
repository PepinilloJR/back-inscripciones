package inscripciones_backend.inscripciones_backend.InscripcionTardia.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import inscripciones_backend.inscripciones_backend.InscripcionTardia.models.InscripcionTardia;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;

@Repository
public interface InscripcionTardiaRepository extends JpaRepository<InscripcionTardia,Long> {

    @Query("SELECT i FROM InscripcionTardia i WHERE i.solicitudInscripcionTardia.id = :solicitudId")
    Optional<InscripcionTardia> findBySolicitud(@Param("solicitudId") Long solicitudId);

    @Query("SELECT i FROM InscripcionTardia i WHERE i.año = :año")
    List<InscripcionTardia> findByAño(@Param("año") String año);
}

