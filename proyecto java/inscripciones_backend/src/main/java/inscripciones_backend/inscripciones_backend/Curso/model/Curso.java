package inscripciones_backend.inscripciones_backend.Curso.model;

import inscripciones_backend.inscripciones_backend.Comision.models.Comision;
import inscripciones_backend.inscripciones_backend.Materia.model.Materia;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(uniqueConstraints = {@UniqueConstraint(columnNames = {"materia_id","comision_id","año"})})
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Curso {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "materia_id", nullable = false)
    private Materia materia;
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "comision_id", nullable = false)
    private Comision comision;
    
    private String cuatrimestre;
    
    private String hora_inicio;
    
    private String hora_fin;
    
    private Integer cupo;
    
    private Integer inscriptos;
    
    private String año;
}
