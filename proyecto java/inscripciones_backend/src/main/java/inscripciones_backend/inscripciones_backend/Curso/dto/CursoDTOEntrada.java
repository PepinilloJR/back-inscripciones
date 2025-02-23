package inscripciones_backend.inscripciones_backend.Curso.dto;

import inscripciones_backend.inscripciones_backend.Materia.model.Materia;

public record CursoDTOEntrada(String materia, String comision, String cuatrimestre, String hora_inicio, String hora_fin, Integer cupo, Integer inscriptos) {

}
