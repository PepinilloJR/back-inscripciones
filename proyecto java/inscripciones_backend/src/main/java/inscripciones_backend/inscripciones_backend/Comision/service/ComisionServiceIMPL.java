package inscripciones_backend.inscripciones_backend.Comision.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import inscripciones_backend.inscripciones_backend.Comision.models.Comision;
import inscripciones_backend.inscripciones_backend.Comision.repository.ComisionRepository;

@Service
public class ComisionServiceIMPL implements ComisionService {

    private final ComisionRepository comisionRepository;

    public ComisionServiceIMPL(ComisionRepository comisionRepository) {
        this.comisionRepository = comisionRepository;
    }

    @Override
    public List<Comision> findAll() {
        return comisionRepository.findAll();
    }

    @Override
    public Optional<Comision> findById(Long id) {
        return comisionRepository.findById(id);
    }

    @Override
    public Comision save(Comision comision) {
        return comisionRepository.save(comision);
    }

    @Override
    public void delete(Long id) {
        comisionRepository.deleteById(id);
    }

    @Override
    public Optional<Comision> findByCodigo(String codigo) {
        return comisionRepository.findByCodigo(codigo);
    }

    
}
