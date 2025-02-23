package inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.service;

import java.util.List;
import java.util.Optional;

import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos.SolicitudInscripcionTardiaDTOEntrada;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos.SolicitudInscripcionTardiaDTOSalida;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;

public interface SolicitudInscripcionTardiaService {
    List<SolicitudInscripcionTardia> findAll();
    Optional<SolicitudInscripcionTardia> findById(Long id);
    List<SolicitudInscripcionTardiaDTOSalida> save(List<SolicitudInscripcionTardiaDTOEntrada> inscripciones);
    void delete(Long id);
    Optional<SolicitudInscripcionTardia> findByAlumnoMateriaAño(Long idAlumno, Long idMateria, String año);
    List<SolicitudInscripcionTardia> findByVisible();
    List<SolicitudInscripcionTardia> findByMateriaCursoVisible(Long materiaId, String codigo);
    List<SolicitudInscripcionTardia> findByMateriaVisible(Long materiaId);
    List<SolicitudInscripcionTardia> findByMateriaCursoTodos(Long materiaId, String codigo);
    List<SolicitudInscripcionTardia> findByMateriaTodos(Long materiaId);
}
