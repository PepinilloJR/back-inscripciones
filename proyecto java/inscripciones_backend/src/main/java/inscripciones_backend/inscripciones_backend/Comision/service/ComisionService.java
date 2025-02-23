package inscripciones_backend.inscripciones_backend.Comision.service;

import java.util.List;
import java.util.Optional;

import inscripciones_backend.inscripciones_backend.Comision.models.Comision;

public interface ComisionService {
    List<Comision> findAll();
    Optional<Comision> findById(Long id);
    Comision save(Comision comision);
    void delete(Long id);
    Optional<Comision> findByCodigo(String codigo);
}
