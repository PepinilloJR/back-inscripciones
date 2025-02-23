package inscripciones_backend.inscripciones_backend.InscripcionTardia.dtos;

import java.util.List;

import inscripciones_backend.inscripciones_backend.InscripcionTardia.models.InscripcionTardia;

public record InscripcionTardiaDTOSalida(InscripcionTardia inscripcionTardia, List<String> errores) {
    
}
