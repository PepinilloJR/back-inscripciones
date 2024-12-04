class Assignable:
    """
    Base class for objects that can have preferences for other objects to be assigned to.
    """
    def __init__(self, id, preferences):
        """
        :param id: Unique identifier for the object.
        :param preferences: A list of preferred IDs in order of priority.
        """
        self.id = id
        self.preferences = preferences


class Containable:
    """
    Base class for objects that can contain other objects, with a limited capacity.
    """
    def __init__(self, id, capacity):
        """
        :param id: Unique identifier for the container.
        :param capacity: Maximum number of objects this container can hold.
        """
        self.id = id
        self.capacity = capacity
        self.objects = []

    def add_object(self, obj):
        """
        Attempts to add an object to the container.
        :param obj: The object to add.
        :return: True if the object was added, False otherwise.
        """
        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True
        return False


def greedy_assignment(assignables, containables):
    """
    Generalized greedy assignment function for assignable objects to containable objects.
    :param assignables: List of Assignable objects to be assigned.
    :param containables: List of Containable objects available for assignment.
    :return: A tuple (remaining_assignables, containables), where remaining_assignables
             is a list of assignables that could not be assigned, and containables
             is the updated list of containers with assigned objects.
    """
    # Create a map of containers for quick access
    containable_map = {containable.id: containable for containable in containables}

    unplaced_assignables = []

    # Assign each assignable to its preferred container, if possible
    for assignable in assignables:
        placed = False
        for preferred_id in assignable.preferences:
            if preferred_id in containable_map:
                containable = containable_map[preferred_id]
                if containable.add_object(assignable):
                    placed = True
                    break
        if not placed:
            unplaced_assignables.append(assignable)

    return unplaced_assignables, containables


def optimize_assignments(unplaced_assignables, containables):
    """
    Generalized optimization function to attempt to minimize unplaced assignables.
    :param unplaced_assignables: List of unplaced assignables after initial greedy assignment.
    :param containables: List of Containable objects with their current assignments.
    :return: A tuple (final_unplaced_assignables, updated_containables).
    """
    containable_map = {containable.id: containable for containable in containables}
    
    # Helper to check if a container has space
    def has_space(containable_id):
        return len(containable_map[containable_id].objects) < containable_map[containable_id].capacity

    # Rearrange items to make room
    for containable in containables:
        if len(containable.objects) == containable.capacity:
            # If container is full, try moving objects to their second preference
            for obj in list(containable.objects):  # Copy the list to avoid mutation during iteration
                if len(containable.objects) <= containable.capacity:
                    break  # Stop once the container is no longer full
                
                for pref_id in obj.preferences[1:]:  # Second-best or lower preferences
                    if has_space(pref_id):
                        containable.objects.remove(obj)
                        containable_map[pref_id].add_object(obj)
                        break

    # Try placing unplaced assignables again
    final_unplaced_assignables = []
    for assignable in unplaced_assignables:
        placed = False
        for preferred_id in assignable.preferences:
            if has_space(preferred_id):
                containable_map[preferred_id].add_object(assignable)
                placed = True
                break
        if not placed:
            final_unplaced_assignables.append(assignable)

    return final_unplaced_assignables, containables
