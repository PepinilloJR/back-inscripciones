package inscripciones_backend.inscripciones_backend.InscripcionTardia.service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Alumno.repository.AlumnoRepository;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;
import inscripciones_backend.inscripciones_backend.Curso.repository.CursoRepository;
import inscripciones_backend.inscripciones_backend.InscripcionTardia.dtos.InscripcionTardiaDTOSalida;
import inscripciones_backend.inscripciones_backend.InscripcionTardia.models.InscripcionTardia;
import inscripciones_backend.inscripciones_backend.InscripcionTardia.repository.InscripcionTardiaRepository;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.repository.SolicitudInscripcionTardiaRepository;
@Service
public class InscripcionTardiaServiceIMPL implements InscripcionTardiaService {

    private final InscripcionTardiaRepository inscripcionTardiaRepository;
    private final AlumnoRepository alumnoRepository;
    private final CursoRepository cursoRepository;
    private final SolicitudInscripcionTardiaRepository solicitudInscripcionTardiaRepository;

    public InscripcionTardiaServiceIMPL(InscripcionTardiaRepository inscripcionTardiaRepository, AlumnoRepository alumnoRepository, CursoRepository cursoRepository,SolicitudInscripcionTardiaRepository solicitudInscripcionTardiaRepository) {
        this.inscripcionTardiaRepository = inscripcionTardiaRepository;
        this.alumnoRepository = alumnoRepository;
        this.cursoRepository = cursoRepository;
        this.solicitudInscripcionTardiaRepository = solicitudInscripcionTardiaRepository;
    }

    @Override
    public List<InscripcionTardia> findAll() {
        return inscripcionTardiaRepository.findAll();
    }

    @Override
    public Optional<InscripcionTardia> findById(Long id) {
        return inscripcionTardiaRepository.findById(id);
    }

    @Override
    @Transactional
    public List<InscripcionTardiaDTOSalida> save(List<InscripcionTardia> inscripcionesTardia) {
        List<InscripcionTardiaDTOSalida> inscripcionTardiaDTOSalidas = new ArrayList<>();
        for (InscripcionTardia inscripcionTardia : inscripcionesTardia) {
            List<String> errores = new ArrayList<>();
            if(inscripcionTardia.getId() != null){
                Optional<InscripcionTardia> inscripcionTardiaBd = inscripcionTardiaRepository.findById(inscripcionTardia.getId());
            if(inscripcionTardiaBd.isPresent()){
                errores.add("Se encuentra registrada una solicitud de inscripcion tardia con los datos especificados");
            }
            }   
            Optional<Alumno> alumno = alumnoRepository.findById(inscripcionTardia.getAlumno().getLegajo());
            if(!alumno.isPresent()){
                errores.add("No se encuentra registrado el alumno con legajo: " + inscripcionTardia.getAlumno().getLegajo());
            }
            else{
                inscripcionTardia.setAlumno(alumno.get());
            }
            LocalDateTime hoy = LocalDateTime.now();
            Integer año = hoy.getYear();
            Optional<Curso> curso = cursoRepository.findByMateriaComisionAño(inscripcionTardia.getCurso().getMateria().getId(), inscripcionTardia.getCurso().getComision().getId(), año.toString());
            if(!curso.isPresent()){
                errores.add("No se encontro un curso con materia: " + inscripcionTardia.getCurso().getMateria().getNombre() + ", " + "comision: " + inscripcionTardia.getCurso().getComision().getCodigo() + ", " + "y año: " + año.toString());
            }
            else{
                if(curso.get().getCupo() - curso.get().getInscriptos() > 0){
                    curso.get().setInscriptos(curso.get().getInscriptos() + 1);
                    inscripcionTardia.setCurso(curso.get());
                    inscripcionTardia.getSolicitudInscripcionTardia().setCurso(curso.get());
                }
                else{
                    errores.add("No hay cupo suficiente para realizar la inscripcion");
                }
            }
            Optional<InscripcionTardia> inscripcion = inscripcionTardiaRepository.findBySolicitud(inscripcionTardia.getSolicitudInscripcionTardia().getId());
            if(inscripcion.isPresent()){
                errores.add("Ya se encuentra registrada la inscripcion solicitada");
            }
            if(errores.isEmpty()){
                List<SolicitudInscripcionTardia> inscripcionesAValidar = solicitudInscripcionTardiaRepository.findByAlumnoMateria(inscripcionTardia.getCurso().getMateria().getId(), inscripcionTardia.getAlumno().getLegajo());
                for (SolicitudInscripcionTardia solicitud : inscripcionesAValidar) {
                    solicitud.setVisible(false);
                }
                solicitudInscripcionTardiaRepository.saveAll(inscripcionesAValidar);
                inscripcionTardia.getSolicitudInscripcionTardia().setVisible(false);
                inscripcionTardia.setAño(año.toString());
                inscripcionTardiaRepository.save(inscripcionTardia);
            }
            else{
                inscripcionTardiaDTOSalidas.add(new InscripcionTardiaDTOSalida(inscripcionTardia, errores)) ;
            }
        }
        return inscripcionTardiaDTOSalidas;
    }

    @Override
    public void delete(Long id) {
        inscripcionTardiaRepository.deleteById(id);
    }

    @Override
    public List<InscripcionTardia> findByAño(String año) {
        return inscripcionTardiaRepository.findByAño(año);
    }

    

    
}
