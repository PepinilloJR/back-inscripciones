package inscripciones_backend.inscripciones_backend.Curso.service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import inscripciones_backend.inscripciones_backend.Comision.models.Comision;
import inscripciones_backend.inscripciones_backend.Comision.repository.ComisionRepository;
import inscripciones_backend.inscripciones_backend.Curso.dto.CursoDTOEntrada;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;
import inscripciones_backend.inscripciones_backend.Curso.repository.CursoRepository;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;
import inscripciones_backend.inscripciones_backend.Materia.repository.MateriaRepository;

@Service
public class CursoServiceIMPL implements CursoService {

    private final CursoRepository cursoRepository;
    private final MateriaRepository materiaRepository;
    private final ComisionRepository comisionRepository;

    public CursoServiceIMPL(CursoRepository cursoRepository, MateriaRepository materiaRepository, ComisionRepository comisionRepository) {
        this.cursoRepository = cursoRepository;
        this.materiaRepository = materiaRepository;
        this.comisionRepository = comisionRepository;
    }

    @Override
    public List<Curso> findAll() {
        return cursoRepository.findAll();
    }

    @Override
    public Optional<Curso> findById(Long id) {
        return cursoRepository.findById(id);
    }

    @Override
    @Transactional
    public List<Curso> save(List<CursoDTOEntrada> cursos) {
        List<Curso> cursosAGuardar = new ArrayList<>();
        for (CursoDTOEntrada curso : cursos) {
            Curso cursoAGuardar = new Curso();
            Optional<Materia> materia = materiaRepository.findByNombre(curso.materia());
            if(materia.isPresent()){
                cursoAGuardar.setMateria(materia.get());
            }
            else{
                Materia materiaAGuardar = new Materia();
                materiaAGuardar.setNombre(curso.materia());
                materiaAGuardar = materiaRepository.save(materiaAGuardar);
                cursoAGuardar.setMateria(materiaAGuardar);
            }
            Optional<Comision> comision = comisionRepository.findByCodigo(curso.comision());
            if(comision.isPresent()){
                cursoAGuardar.setComision(comision.get());
            }
            else{
                Comision comisionAGuardar = new Comision();
                comisionAGuardar.setCodigo(curso.comision());
                comisionAGuardar = comisionRepository.save(comisionAGuardar);
                cursoAGuardar.setComision(comisionAGuardar);
            }
            LocalDateTime hoy = LocalDateTime.now();
            Integer año = hoy.getYear();
            cursoAGuardar.setAño(año.toString());
            cursoAGuardar.setCuatrimestre(curso.cuatrimestre());
            cursoAGuardar.setCupo(curso.cupo());
            cursoAGuardar.setHora_fin(curso.hora_fin());
            cursoAGuardar.setHora_inicio(curso.hora_inicio());
            cursoAGuardar.setInscriptos(curso.inscriptos());
            Optional<Curso> cursoBd = cursoRepository.findByMateriaComisionAño(cursoAGuardar.getMateria().getId(), cursoAGuardar.getComision().getId(), cursoAGuardar.getAño());
            if(!cursoBd.isPresent()){
                cursosAGuardar.add(cursoAGuardar);
            }
        }
        return cursoRepository.saveAll(cursosAGuardar);
    }

    @Override
    public void delete(Long id) {
        cursoRepository.deleteById(id);
    }

    @Override
    public Optional<Curso> findByMateriaComision(Long materiaId, Long ComisionId, String año) {
        return cursoRepository.findByMateriaComisionAño(materiaId, ComisionId, año);
    }
    @Override
    public List<Curso> findByMateriaId(Long materiaId) {
        return cursoRepository.findByMateria(materiaId);
    }

    
}
