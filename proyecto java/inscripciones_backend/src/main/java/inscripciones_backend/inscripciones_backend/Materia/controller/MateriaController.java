package inscripciones_backend.inscripciones_backend.Materia.controller;

import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import inscripciones_backend.inscripciones_backend.Excepciones.EntityAlreadyExistsException;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;
import inscripciones_backend.inscripciones_backend.Materia.service.MateriaService;
import jakarta.websocket.server.PathParam;

@RestController
@CrossOrigin
@RequestMapping("/materia")
public class MateriaController {

    private final MateriaService materiaService;

    public MateriaController(MateriaService materiaService) {
        this.materiaService = materiaService;
    }

    @GetMapping
    public ResponseEntity<List<Materia>> getAllMaterias(){
        List<Materia> materias = materiaService.findAll();
        return new ResponseEntity<>(materias,HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Materia> getMateria(@PathVariable Long id){
        Optional<Materia> materia = materiaService.findById(id);
        if(materia.isPresent()){
            Materia materiaBd = materia.orElseThrow();
            return new ResponseEntity<>(materiaBd,HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @PostMapping
    public ResponseEntity<Materia> saveMateria(@RequestBody Materia materia) throws EntityAlreadyExistsException{
        Materia materiaGuardada = materiaService.save(materia);
        return new ResponseEntity<>(materiaGuardada,HttpStatus.CREATED);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteMateria(@PathVariable Long id){
        Optional<Materia> materia = materiaService.findById(id);
        if(materia.isPresent()){
            materiaService.delete(id);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
