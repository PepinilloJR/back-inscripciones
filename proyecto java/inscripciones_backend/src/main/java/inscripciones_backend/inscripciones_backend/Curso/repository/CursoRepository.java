package inscripciones_backend.inscripciones_backend.Curso.repository;
import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import inscripciones_backend.inscripciones_backend.Curso.model.Curso;

@Repository
public interface CursoRepository extends JpaRepository<Curso,Long> {

    @Query("SELECT c FROM Curso c WHERE c.materia.id = :materiaId AND c.comision.id = :comisionId AND c.año = :año")
    Optional<Curso> findByMateriaComisionAño(@Param("materiaId") Long materiaId, @Param("comisionId") Long comisionId, @Param("año") String año);

    @Query("SELECT c FROM Curso c WHERE c.materia.id = :materiaId")
    List<Curso> findByMateria(@Param("materiaId") Long materiaId);
}
