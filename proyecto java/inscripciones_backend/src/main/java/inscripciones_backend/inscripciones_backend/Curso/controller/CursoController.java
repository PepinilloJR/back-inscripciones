package inscripciones_backend.inscripciones_backend.Curso.controller;

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

import inscripciones_backend.inscripciones_backend.Curso.dto.CursoDTOEntrada;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;
import inscripciones_backend.inscripciones_backend.Curso.service.CursoService;
import jakarta.validation.Valid;

@RestController
@CrossOrigin
@RequestMapping("/curso")
public class CursoController {

    private final CursoService cursoService;

    
    public CursoController(CursoService cursoService) {
        this.cursoService = cursoService;
    }


    @GetMapping
    public ResponseEntity<List<Curso>> getAllCursos(){
        List<Curso> cursos = cursoService.findAll();
        return new ResponseEntity<>(cursos, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Curso> getCurso(@PathVariable Long id){
        Optional<Curso> curso = cursoService.findById(id);
        if(curso.isPresent()){
            return new ResponseEntity<>(curso.orElseThrow(),HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    @GetMapping("/materia/{id}")
    public ResponseEntity<List<Curso>> getCursoByMateria(@PathVariable Long id){
        List<Curso> cursos = cursoService.findByMateriaId(id);
        return new ResponseEntity<>(cursos,HttpStatus.OK);
    }


    @PostMapping
    public ResponseEntity<List<Curso>> saveCursos(@RequestBody List<CursoDTOEntrada> cursos){
        List<Curso > cursosAGuardar = cursoService.save(cursos);
        return new ResponseEntity<>(cursosAGuardar,HttpStatus.CREATED);    
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCurso(@PathVariable Long id){
        Optional<Curso> curso = cursoService.findById(id);
        if(curso.isPresent()){
           cursoService.delete(id);
           return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
