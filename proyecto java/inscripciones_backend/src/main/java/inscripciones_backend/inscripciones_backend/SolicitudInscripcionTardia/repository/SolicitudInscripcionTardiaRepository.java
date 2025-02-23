package inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;

@Repository
public interface SolicitudInscripcionTardiaRepository extends JpaRepository<SolicitudInscripcionTardia,Long>{

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.alumno.id = :alumnoId AND i.materia.id = :materiaId AND i.año = :año")
    Optional<SolicitudInscripcionTardia> findByAlumnoMateriaAño(@Param("alumnoId") Long alumnoId, @Param("materiaId") Long materiaId, @Param("año") String año);

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.alumno.id = :alumnoId AND i.materia.id = :materiaId")
    List<SolicitudInscripcionTardia> findByAlumnoMateria(@Param("materiaId") Long materiaId, @Param("alumnoId") Long alumnoId);

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.visible = true")
    List<SolicitudInscripcionTardia> findByVisible();

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.materia.id = :materiaId AND i.curso.comision.codigo = :codigo AND i.visible = true")
    List<SolicitudInscripcionTardia> findByMateriaCursoVisible(@Param("materiaId") Long id, @Param("codigo") String codigo);

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.materia.id = :materiaId AND i.visible = true")
    List<SolicitudInscripcionTardia> findByMateriaVisible(@Param("materiaId") Long id);

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.materia.id = :materiaId AND i.curso.comision.codigo = :codigo")
    List<SolicitudInscripcionTardia> findByMateriaCursoTodos(@Param("materiaId") Long id, @Param("codigo") String codigo);

    @Query("SELECT i FROM SolicitudInscripcionTardia i WHERE i.materia.id = :materiaId")
    List<SolicitudInscripcionTardia> findByMateriaTodos(@Param("materiaId") Long id);
}
