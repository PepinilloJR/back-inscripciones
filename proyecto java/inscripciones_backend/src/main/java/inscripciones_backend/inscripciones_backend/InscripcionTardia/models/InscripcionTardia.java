package inscripciones_backend.inscripciones_backend.InscripcionTardia.models;

import org.hibernate.annotations.DialectOverride.JoinFormula;

import inscripciones_backend.inscripciones_backend.Alumno.model.Alumno;
import inscripciones_backend.inscripciones_backend.Comision.models.Comision;
import inscripciones_backend.inscripciones_backend.Curso.model.Curso;
import inscripciones_backend.inscripciones_backend.SolicitudInscripcionTardia.models.SolicitudInscripcionTardia;
import jakarta.annotation.Generated;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
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
public class InscripcionTardia {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @OneToOne(cascade = CascadeType.MERGE, orphanRemoval = true)
    @JoinColumn(name = "solicitudInscripcionId")
    private SolicitudInscripcionTardia solicitudInscripcionTardia;
    @ManyToOne(cascade = CascadeType.MERGE)
    @JoinColumn(name = "alumnoId")
    private Alumno alumno;
    @ManyToOne(cascade = CascadeType.MERGE)
    @JoinColumn(name = "cursoId")
    private Curso curso;
    private String estado;
    private String año;

}
