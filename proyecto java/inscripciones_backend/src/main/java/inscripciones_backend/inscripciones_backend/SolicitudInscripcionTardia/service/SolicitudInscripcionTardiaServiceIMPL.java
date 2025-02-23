package inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Alumno.repository.AlumnoRepository;
import inscripciones_backend.inscripciones_backend.Comision.models.Comision;
import inscripciones_backend.inscripciones_backend.Comision.repository.ComisionRepository;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;
import inscripciones_backend.inscripciones_backend.Curso.repository.CursoRepository;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;
import inscripciones_backend.inscripciones_backend.Materia.repository.MateriaRepository;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos.SolicitudInscripcionTardiaDTOEntrada;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos.SolicitudInscripcionTardiaDTOSalida;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.repository.SolicitudInscripcionTardiaRepository;

@Service
public class SolicitudInscripcionTardiaServiceIMPL implements SolicitudInscripcionTardiaService{

    private final SolicitudInscripcionTardiaRepository inscripcionTardiaRepository;
    private final AlumnoRepository alumnoRepository;
    private final CursoRepository cursoRepository;
    private final MateriaRepository materiaRepository;
    private final ComisionRepository comisionRepository;

    public SolicitudInscripcionTardiaServiceIMPL(SolicitudInscripcionTardiaRepository inscripcionTardiaRepository, AlumnoRepository alumnoRepository, CursoRepository cursoRepository, MateriaRepository materiaRepository, ComisionRepository comisionRepository) {
        this.inscripcionTardiaRepository = inscripcionTardiaRepository;
        this.alumnoRepository = alumnoRepository;
        this.cursoRepository = cursoRepository;
        this.materiaRepository = materiaRepository;
        this.comisionRepository = comisionRepository;
    }

    @Override
    public List<SolicitudInscripcionTardia> findAll() {
        return inscripcionTardiaRepository.findAll();
    }

    @Override
    public Optional<SolicitudInscripcionTardia> findById(Long id) {
        return inscripcionTardiaRepository.findById(id);
    }

    @Override
    @Transactional
    public List<SolicitudInscripcionTardiaDTOSalida> save(List<SolicitudInscripcionTardiaDTOEntrada> inscripciones) {
        List<SolicitudInscripcionTardia> solicitudesAGuardar = new ArrayList<>();
        List<SolicitudInscripcionTardiaDTOSalida> solicitudesNoGuardadas = new ArrayList<>();
        for (SolicitudInscripcionTardiaDTOEntrada solicitudinscripcionTardia : inscripciones) {
            SolicitudInscripcionTardia solicitudAGuardar = new SolicitudInscripcionTardia();
            List<String> errores = new ArrayList<>();
            Optional<Alumno> alumno = alumnoRepository.findByNombreApellido(solicitudinscripcionTardia.nombre(), solicitudinscripcionTardia.apellido());
            if(alumno.isPresent()){
                solicitudAGuardar.setAlumno(alumno.get());
            }
            else{
                Alumno alumnoAGuardar = new Alumno();
                alumnoAGuardar.setLegajo(solicitudinscripcionTardia.legajo());
                alumnoAGuardar.setNombre(solicitudinscripcionTardia.nombre());
                alumnoAGuardar.setApellido(solicitudinscripcionTardia.apellido());
                alumnoAGuardar = alumnoRepository.save(alumnoAGuardar);
                solicitudAGuardar.setAlumno(alumnoAGuardar);
            }
            LocalDateTime hoy = LocalDateTime.now();
            Integer año = hoy.getYear();
            Materia materia = new Materia();
            Optional<Materia> materiaBd = materiaRepository.findByNombre(solicitudinscripcionTardia.materia());
            if(materiaBd.isPresent()){
                materia = materiaBd.get();
                solicitudAGuardar.setMateria(materia);
            }
            else{
                errores.add("No se encontro ninguna materia con el nombre: " + solicitudinscripcionTardia.materia());
            }
            Comision comision = new Comision();
            Optional<Comision> comisionBd = comisionRepository.findByCodigo(solicitudinscripcionTardia.curso());
            if(comisionBd.isPresent()){
                comision = comisionBd.get();
            }
            else{
                errores.add("No se encontro ninguna comision con el codigo: " + solicitudinscripcionTardia.curso());
            }
            Optional<Curso> curso = cursoRepository.findByMateriaComisionAño(materia.getId(), comision.getId(), año.toString());
            if(curso.isPresent()){
                solicitudAGuardar.setCurso(curso.get());
            }
            else{
                errores.add("No se encontro un curso con la materia: " + solicitudinscripcionTardia.materia() + ", " + "comision: " + solicitudinscripcionTardia.curso() + ", " + "y año: " + año.toString());
            }
            Optional<Comision> comisionuno = comisionRepository.findByCodigo(solicitudinscripcionTardia.comision1());
            if(comisionuno.isPresent()){
                solicitudAGuardar.setComision1(comisionuno.get());
            }
            else{
                errores.add("No se encontro una comision con el codigo: " + solicitudinscripcionTardia.comision1());
            }
            Optional<Comision> comisiondos = comisionRepository.findByCodigo(solicitudinscripcionTardia.comision2());
            if(comisiondos.isPresent()){
                solicitudAGuardar.setComision2(comisiondos.get());
            }
            else{
                errores.add("No se encontro una comision con el codigo: " + solicitudinscripcionTardia.comision2());
            }
            solicitudAGuardar.setCondicion(solicitudinscripcionTardia.condicion());
            solicitudAGuardar.setVisible(true);
            solicitudAGuardar.setAño(año.toString());
            if(!errores.isEmpty()){
                solicitudAGuardar.setId(solicitudinscripcionTardia.id());
                SolicitudInscripcionTardiaDTOSalida solicitudInscripcionTardiaDTOSalida = new SolicitudInscripcionTardiaDTOSalida(solicitudAGuardar, errores);
                solicitudesNoGuardadas.add(solicitudInscripcionTardiaDTOSalida);
            }
            else{
                Optional<SolicitudInscripcionTardia> inscripcionBd = inscripcionTardiaRepository.findByAlumnoMateriaAño(solicitudAGuardar.getAlumno().getLegajo(), solicitudAGuardar.getCurso().getMateria().getId(), año.toString());
                if(!inscripcionBd.isPresent()){
                    solicitudesAGuardar.add(solicitudAGuardar);
                }
            }
        } 
        inscripcionTardiaRepository.saveAll(solicitudesAGuardar);
        return solicitudesNoGuardadas;
    }

    @Override
    public void delete(Long id) {
        inscripcionTardiaRepository.deleteById(id);
    }

    @Override
    public Optional<SolicitudInscripcionTardia> findByAlumnoMateriaAño(Long idAlumno, Long idMateria, String año) {
        return inscripcionTardiaRepository.findByAlumnoMateriaAño(idAlumno, idMateria, año);
    }

    @Override
    public List<SolicitudInscripcionTardia> findByVisible() {
        return inscripcionTardiaRepository.findByVisible();
    }

    @Override
    public List<SolicitudInscripcionTardia> findByMateriaCursoVisible(Long materiaId, String codigo) {
        return inscripcionTardiaRepository.findByMateriaCursoVisible(materiaId, codigo);
    }

    @Override
    public List<SolicitudInscripcionTardia> findByMateriaVisible(Long materiaId) {
        return inscripcionTardiaRepository.findByMateriaVisible(materiaId);
    }

    @Override
    public List<SolicitudInscripcionTardia> findByMateriaCursoTodos(Long materiaId, String codigo) {
        return inscripcionTardiaRepository.findByMateriaCursoTodos(materiaId, codigo);
    }

    @Override
    public List<SolicitudInscripcionTardia> findByMateriaTodos(Long materiaId) {
        return inscripcionTardiaRepository.findByMateriaTodos(materiaId);
    }

    
}
