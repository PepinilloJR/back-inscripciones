package inscripciones_backend.inscripciones_backend.InscripcionTardia.service;

import java.util.List;
import java.util.Optional;

import inscripciones_backend.inscripciones_backend.InscripcionTardia.dtos.InscripcionTardiaDTOSalida;
import inscripciones_backend.inscripciones_backend.InscripcionTardia.models.InscripcionTardia;

public interface InscripcionTardiaService {
    List<InscripcionTardia> findAll();
    Optional<InscripcionTardia> findById(Long id);
    List<InscripcionTardiaDTOSalida> save(List<InscripcionTardia> inscripcionesTardia);
    void delete(Long id);
    List<InscripcionTardia> findByAño(String año);
    
}
