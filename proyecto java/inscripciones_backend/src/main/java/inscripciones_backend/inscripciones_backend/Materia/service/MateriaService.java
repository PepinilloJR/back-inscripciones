package inscripciones_backend.inscripciones_backend.Materia.service;

import java.util.List;
import java.util.Optional;

import inscripciones_backend.inscripciones_backend.Excepciones.EntityAlreadyExistsException;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;

public interface MateriaService {
    List<Materia> findAll();
    Optional<Materia> findById(Long id);
    Materia save(Materia materia) throws EntityAlreadyExistsException;
    void delete(Long id);
    Optional<Materia> findByNombre(String nombre);
}
