package inscripciones_backend.inscripciones_backend.Excepciones;

public class EntityAlreadyExistsException extends Exception {
    public EntityAlreadyExistsException(String message) {
        super(message);
    }
}
