package inscripciones_backend.inscripciones_backend.Materia.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import inscripciones_backend.inscripciones_backend.Excepciones.EntityAlreadyExistsException;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;
import inscripciones_backend.inscripciones_backend.Materia.repository.MateriaRepository;

@Service
public class MateriaServiceIMPL implements MateriaService{

    private final MateriaRepository materiaRepository;

    public MateriaServiceIMPL(MateriaRepository materiaRepository) {
        this.materiaRepository = materiaRepository;
    }

    @Override
    public List<Materia> findAll() {
        return materiaRepository.findAll();
    }

    @Override
    public Optional<Materia> findById(Long id) {
        return materiaRepository.findById(id);
    }

    @Override
    public Materia save(Materia materia) throws EntityAlreadyExistsException {
        Optional<Materia> materiaBd = materiaRepository.findByNombre(materia.getNombre());
        if(!materiaBd.isPresent()){
            return materiaRepository.save(materia);
        }
        else{
            throw new EntityAlreadyExistsException("Ya se encuentra registrada una materia con el nombre: " + materia.getNombre());
        }
    }

    @Override
    public void delete(Long id) {
        materiaRepository.deleteById(id);
    }

    @Override
    public Optional<Materia> findByNombre(String nombre) {
        return materiaRepository.findByNombre(nombre);

    }

    
}
