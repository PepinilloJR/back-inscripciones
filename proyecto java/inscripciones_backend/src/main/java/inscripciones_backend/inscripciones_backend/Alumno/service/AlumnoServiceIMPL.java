package inscripciones_backend.inscripciones_backend.Alumno.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Alumno.repository.AlumnoRepository;

@Service
public class AlumnoServiceIMPL implements AlumnoService {

    private final AlumnoRepository alumnoRepository;

    public AlumnoServiceIMPL(AlumnoRepository alumnoRepository) {
        this.alumnoRepository = alumnoRepository;
    }

    @Override
    public List<Alumno> findAll() {
        return alumnoRepository.findAll();
    }

    @Override
    public Optional<Alumno> findById(Long id) {
        return alumnoRepository.findById(id);
    }

    @Override
    public Alumno save(Alumno alumno) {
        return alumnoRepository.save(alumno);    
    }

    @Override
    public void delete(Long id) {
        alumnoRepository.deleteById(id);
    }

    @Override
    public Optional<Alumno> existeNombreApellido(String nombre, String apellido) {
        return alumnoRepository.findByNombreApellido(nombre, apellido);
    }

    
}
