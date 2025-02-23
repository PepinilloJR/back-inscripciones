package inscripciones_backend.inscripciones_backend.Alumno.controller;

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

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Alumno.service.AlumnoService;

@RestController
@CrossOrigin
@RequestMapping("/alumno")
public class AlumnoController {

    private final AlumnoService alumnoService;

    public AlumnoController(AlumnoService alumnoService) {
        this.alumnoService = alumnoService;
    }

    @GetMapping
    public ResponseEntity<List<Alumno>> getAllAlumnos(){
        List<Alumno> alumnos = alumnoService.findAll();
        return new ResponseEntity<>(alumnos, HttpStatus.OK);
    }

    @GetMapping("/{legajo}")
    public ResponseEntity<Alumno> getAlumno(@PathVariable Long legajo){
        Optional<Alumno> alumno = alumnoService.findById(legajo);
        if(alumno.isPresent()){
            Alumno alumnoBd = alumno.orElseThrow();
            return new ResponseEntity<>(alumnoBd,HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @PostMapping
    public ResponseEntity<Alumno> saveAlumno(@RequestBody Alumno alumno){
        Alumno alumnoGuardado = alumnoService.save(alumno);
        return new ResponseEntity<>(alumnoGuardado,HttpStatus.CREATED);
    }

    @DeleteMapping("/{legajo}")
    public ResponseEntity<Void> deleteAlumno(@PathVariable Long legajo){
        Optional<Alumno> alumno = alumnoService.findById(legajo);
        if(alumno.isPresent()){
            alumnoService.delete(legajo);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
