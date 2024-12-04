class Entity:
    def __init__(self, id, preferences):
        """
        Represents an entity to be assigned.
        :param id: Unique identifier for the entity.
        :param preferences: A list of preferred container IDs in order of priority.
        """
        self.id = id
        self.preferences = preferences


class Container:
    def __init__(self, id, capacity):
        """
        Represents a container with a limited capacity.
        :param id: Unique identifier for the container.
        :param capacity: Maximum number of entities this container can hold.
        """
        self.id = id
        self.capacity = capacity
        self.entities = []

    def add_entity(self, entity):
        """
        Attempts to add an entity to the container.
        :param entity: The entity to add.
        :return: True if the entity was added, False otherwise.
        """
        if len(self.entities) < self.capacity:
            self.entities.append(entity)
            return True
        return False


def greedy_assignment(entities, containers):
    """
    Assigns entities to containers using a greedy approach.
    :param entities: List of Entity objects to be assigned.
    :param containers: List of Container objects available for assignment.
    :return: A tuple (remaining_entities, containers), where remaining_entities
             is a list of entities that could not be assigned, and containers
             is the updated list of containers with assigned entities.
    """
    # Create a map of containers for quick access
    container_map = {container.id: container for container in containers}

    unplaced_entities = []

    # Assign each entity to its preferred container, if possible
    for entity in entities:
        placed = False
        for preferred_id in entity.preferences:
            if preferred_id in container_map:
                container = container_map[preferred_id]
                if container.add_entity(entity):
                    placed = True
                    break
        if not placed:
            unplaced_entities.append(entity)

    return unplaced_entities, containers


def optimize_assignments(unplaced_entities, containers):
    """
    Attempts to optimize assignments by rearranging entities to minimize the number of unplaced entities.
    :param unplaced_entities: List of unplaced entities after initial greedy assignment.
    :param containers: List of Container objects with their current assignments.
    :return: A tuple (final_unplaced_entities, updated_containers).
    """
    container_map = {container.id: container for container in containers}
    
    # Helper to check if a container has space
    def has_space(container_id):
        return len(container_map[container_id].entities) < container_map[container_id].capacity

    # Rearrange items to make room
    for container in containers:
        if len(container.entities) == container.capacity:
            # If container is full, try moving entities to their second preference
            for entity in list(container.entities):  # Copy the list to avoid mutation during iteration
                if len(container.entities) <= container.capacity:
                    break  # Stop once the container is no longer full
                
                for pref_id in entity.preferences[1:]:  # Second-best or lower preferences
                    if has_space(pref_id):
                        container.entities.remove(entity)
                        container_map[pref_id].add_entity(entity)
                        break

    # Try placing unplaced entities again
    final_unplaced_entities = []
    for entity in unplaced_entities:
        placed = False
        for preferred_id in entity.preferences:
            if has_space(preferred_id):
                container_map[preferred_id].add_entity(entity)
                placed = True
                break
        if not placed:
            final_unplaced_entities.append(entity)

    return final_unplaced_entities, containers




