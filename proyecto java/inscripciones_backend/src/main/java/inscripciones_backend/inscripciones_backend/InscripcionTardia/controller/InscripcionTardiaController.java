package inscripciones_backend.inscripciones_backend.InscripcionTardia.controller;

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

import inscripciones_backend.inscripciones_backend.InscripcionTardia.dtos.InscripcionTardiaDTOSalida;
import inscripciones_backend.inscripciones_backend.InscripcionTardia.models.InscripcionTardia;
import inscripciones_backend.inscripciones_backend.InscripcionTardia.service.InscripcionTardiaService;

@RestController
@CrossOrigin
@RequestMapping("/inscripcionTardia")
public class InscripcionTardiaController {

    private final InscripcionTardiaService inscripcionTardiaService;

    public InscripcionTardiaController(InscripcionTardiaService inscripcionTardiaService) {
        this.inscripcionTardiaService = inscripcionTardiaService;
    }

    @GetMapping
    public ResponseEntity<List<InscripcionTardia>> getAllInscripcionesTardias(){
        List<InscripcionTardia> inscripcionesTardias = inscripcionTardiaService.findAll();
        return new ResponseEntity<>(inscripcionesTardias,HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<InscripcionTardia> getInscripcionTardia(@PathVariable Long id){
        Optional<InscripcionTardia> inscripcionTardia = inscripcionTardiaService.findById(id);
        if(inscripcionTardia.isPresent()){
            InscripcionTardia inscripcionTardiaBd = inscripcionTardia.orElseThrow();
            return new ResponseEntity<>(inscripcionTardiaBd,HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @GetMapping("año/{año}")
    public ResponseEntity<List<InscripcionTardia>> getAllInscripcionesPorAño(@PathVariable String año){
        List<InscripcionTardia> inscripcionesTardias = inscripcionTardiaService.findByAño(año);
        return new ResponseEntity<>(inscripcionesTardias,HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<List<InscripcionTardiaDTOSalida>> saveInscripcionesTardias(@RequestBody List<InscripcionTardia> inscripciones){
        List<InscripcionTardiaDTOSalida> inscripcionesFallidas = inscripcionTardiaService.save(inscripciones);
        return new ResponseEntity<>(inscripcionesFallidas,HttpStatus.CREATED);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteInscripcionTardia(@PathVariable Long id){
        Optional<InscripcionTardia> inscripcion = inscripcionTardiaService.findById(id);
        if(inscripcion.isPresent()){
            inscripcionTardiaService.delete(id);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
