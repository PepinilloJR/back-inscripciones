package inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.dtos;

import java.util.List;

import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;

public record SolicitudInscripcionTardiaDTOSalida(SolicitudInscripcionTardia solicitudInscripcionTardia, List<String> errores) {

}
