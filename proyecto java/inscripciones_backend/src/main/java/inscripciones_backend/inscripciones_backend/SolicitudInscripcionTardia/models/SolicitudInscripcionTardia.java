package inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Comision.models.Comision;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class SolicitudInscripcionTardia {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "alumno_id", nullable = false)
    private Alumno alumno;
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "curso_id", nullable = false)
    private Curso curso;
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "comisionuno_id", nullable = false)
    private Comision comision1;
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "comisiondos_id", nullable = false)
    private Comision comision2;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "materia_id", nullable = false)
    private Materia materia;

    private String año;
    private String condicion;
    private boolean visible;
}
