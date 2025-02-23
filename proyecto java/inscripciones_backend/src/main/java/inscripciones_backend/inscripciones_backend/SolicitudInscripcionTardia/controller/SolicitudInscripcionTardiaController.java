package inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.controller;

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

import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos.SolicitudInscripcionTardiaDTOEntrada;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos.SolicitudInscripcionTardiaDTOSalida;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.service.SolicitudInscripcionTardiaService;

@RestController
@CrossOrigin
@RequestMapping("/solicitudInscripcionTardia")
public class SolicitudInscripcionTardiaController {

    private final SolicitudInscripcionTardiaService solciitudInscripcionTardiaService;

    public SolicitudInscripcionTardiaController(SolicitudInscripcionTardiaService solciitudInscripcionTardiaService) {
        this.solciitudInscripcionTardiaService = solciitudInscripcionTardiaService;
    }

    @GetMapping
    public ResponseEntity<List<SolicitudInscripcionTardia>> getAllSolicitudes(){
        List<SolicitudInscripcionTardia> solicitudes = solciitudInscripcionTardiaService.findAll();
        return new ResponseEntity<>(solicitudes,HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<SolicitudInscripcionTardia> getSolicitud(@PathVariable Long id){
        Optional<SolicitudInscripcionTardia> solicitud = solciitudInscripcionTardiaService.findById(id);
        if(solicitud.isPresent()){
            return new ResponseEntity<>(solicitud.get(),HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @GetMapping("/materia/{materiaId}/curso/{codigoCurso}/visible")
    public ResponseEntity<List<SolicitudInscripcionTardia>> getInscripcionesPorMateriaCursoVisibles(@PathVariable Long materiaId, @PathVariable String codigoCurso){
        List<SolicitudInscripcionTardia> solicitudes = solciitudInscripcionTardiaService.findByMateriaCursoVisible(materiaId, codigoCurso);
        return new ResponseEntity<>(solicitudes, HttpStatus.OK);
    }

    @GetMapping("/materia/{materiaId}/visible")
    public ResponseEntity<List<SolicitudInscripcionTardia>> getInscripcionesPorMateriaVisibles(@PathVariable Long materiaId){
        List<SolicitudInscripcionTardia> solicitudes = solciitudInscripcionTardiaService.findByMateriaVisible(materiaId);
        return new ResponseEntity<>(solicitudes, HttpStatus.OK);
    }

    @GetMapping("/materia/{materiaId}/curso/{codigoCurso}/all")
    public ResponseEntity<List<SolicitudInscripcionTardia>> getAllInscripcionesPorMateriaCurso(@PathVariable Long materiaId, @PathVariable String codigoCurso){
        List<SolicitudInscripcionTardia> solicitudes = solciitudInscripcionTardiaService.findByMateriaCursoVisible(materiaId, codigoCurso);
        return new ResponseEntity<>(solicitudes, HttpStatus.OK);
    }

    @GetMapping("/materia/{materiaId}/all")
    public ResponseEntity<List<SolicitudInscripcionTardia>> getAllInscripcionesPorMateria(@PathVariable Long materiaId){
        List<SolicitudInscripcionTardia> solicitudes = solciitudInscripcionTardiaService.findByMateriaTodos(materiaId);
        return new ResponseEntity<>(solicitudes, HttpStatus.OK);
    }

    @GetMapping("/visible")
    public ResponseEntity<List<SolicitudInscripcionTardia>> getSolicitudesVisibles(){
        List<SolicitudInscripcionTardia> solicitudes = solciitudInscripcionTardiaService.findByVisible();
        return new ResponseEntity<>(solicitudes,HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<List<SolicitudInscripcionTardiaDTOSalida>> saveInscripcionesTardias(@RequestBody List<SolicitudInscripcionTardiaDTOEntrada> inscripciones){
        List<SolicitudInscripcionTardiaDTOSalida> inscripcionesGuardadas = solciitudInscripcionTardiaService.save(inscripciones);
        return new ResponseEntity<>(inscripcionesGuardadas,HttpStatus.CREATED);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSolicitudesInscripcion(@PathVariable Long id){
        Optional<SolicitudInscripcionTardia> solicitud = solciitudInscripcionTardiaService.findById(id);
        if(solicitud.isPresent()){
            solciitudInscripcionTardiaService.delete(id);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);
        }
        else
        {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

}
