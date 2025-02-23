package inscripciones_backend.inscripciones_backend.Alumno.service;

import java.util.List;
import java.util.Optional;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;

public interface AlumnoService {
    List<Alumno> findAll();
    Optional<Alumno> findById(Long id);
    Alumno save(Alumno alumno);
    void delete(Long id);
    Optional<Alumno> existeNombreApellido(String nombre, String apellido);
}
