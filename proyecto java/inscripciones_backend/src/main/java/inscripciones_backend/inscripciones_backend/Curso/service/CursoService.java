package inscripciones_backend.inscripciones_backend.Curso.service;

import java.util.List;
import java.util.Optional;

import inscripciones_backend.inscripciones_backend.Curso.dto.CursoDTOEntrada;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;

public interface CursoService {
    List<Curso> findAll();
    Optional<Curso> findById(Long id);
    List<Curso> save(List<CursoDTOEntrada> curso);
    void delete(Long id);
    Optional<Curso> findByMateriaComision(Long materiaId, Long ComisionId, String año);
    List<Curso> findByMateriaId(Long materiaId);
}
