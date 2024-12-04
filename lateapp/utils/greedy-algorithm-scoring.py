
# Updated Greedy Assignment with Dynamic Scoring
def greedy_assignment_with_scoring(entities, containers, scoring_function):
    """
    Assign entities to containers using a greedy approach with dynamic scoring.
    :param entities: List of Entity objects to be assigned.
    :param containers: List of Container objects available for assignment.
    :param scoring_function: A function that computes a score for an entity-container pair.
    :return: A tuple (unplaced_entities, containers) after the greedy assignment.
    """
    container_map = {container.id: container for container in containers}
    unplaced_entities = []

    for entity in entities:
        # Score and sort containers dynamically for this entity
        scored_containers = sorted(
            [(container.id, scoring_function(entity, container)) for container in containers],
            key=lambda x: x[1],  # Sort by score (higher is better)
            reverse=True
        )

        placed = False
        for container_id, score in scored_containers:
            if score > 0 and container_map[container_id].add_entity(entity):
                placed = True
                break

        if not placed:
            unplaced_entities.append(entity)

    return unplaced_entities, containers


# Updated Optimization Function with Dynamic Scoring
def optimize_assignments_with_scoring(unplaced_entities, containers, scoring_function):
    """
    Optimize assignments by rearranging entities based on dynamic scoring.
    :param unplaced_entities: List of unplaced entities after initial greedy assignment.
    :param containers: List of Container objects with their current assignments.
    :param scoring_function: A function that computes a score for an entity-container pair.
    :return: A tuple (final_unplaced_entities, updated_containers).
    """
    container_map = {container.id: container for container in containers}

    # Helper to check if a container has space
    def has_space(container_id):
        return len(container_map[container_id].entities) < container_map[container_id].capacity

    # Rearrange items to make room
    for container in containers:
        for entity in list(container.entities):
            # Score all alternative containers for this entity
            scored_containers = sorted(
                [(c.id, scoring_function(entity, c)) for c in containers if c.id != container.id],
                key=lambda x: x[1],
                reverse=True
            )

            for new_container_id, score in scored_containers:
                if score > 0 and has_space(new_container_id):
                    # Move the entity to a better container
                    container.entities.remove(entity)
                    container_map[new_container_id].add_entity(entity)
                    break

    # Try placing unplaced entities again
    final_unplaced_entities = []
    for entity in unplaced_entities:
        scored_containers = sorted(
            [(container.id, scoring_function(entity, container)) for container in containers],
            key=lambda x: x[1],
            reverse=True
        )

        placed = False
        for container_id, score in scored_containers:
            if score > 0 and has_space(container_id):
                container_map[container_id].add_entity(entity)
                placed = True
                break

        if not placed:
            final_unplaced_entities.append(entity)

    return final_unplaced_entities, containers


def scoring_function(entity, container):
    """
    Computes a dynamic score for assigning an entity to a container.
    :param entity: The entity being considered.
    :param container: The container being scored.
    :return: A score (higher is better).
    """
    preference_score = 0
    if container.id == entity.preferences[0]:
        preference_score = 10  # High score for best preference
    elif container.id == entity.preferences[1]:
        preference_score = 5  # Lower score for second preference

    remaining_capacity_score = container.capacity - len(container.entities)
    return preference_score + remaining_capacity_score
