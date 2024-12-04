class Item:
    def __init__(self, id, best_box, second_best_box):
        self.id = id
        self.best_box = best_box
        self.second_best_box = second_best_box

class Box:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

def sort_items_to_boxes(items, boxes):
    unplaced_items = []
    
    # Create a map of boxes for quick access
    box_map = {box.id: box for box in boxes}
    
    # Attempt to place items in their best box first
    for item in items:
        best_box = box_map[item.best_box]
        second_best_box = box_map[item.second_best_box]
        
        if best_box.add_item(item):
            continue
        elif second_best_box.add_item(item):
            continue
        else:
            unplaced_items.append(item)
    
    return unplaced_items


def optimize_placements(items, boxes):
    box_map = {box.id: box for box in boxes}

    # Helper to check box capacity
    def can_fit(box_id):
        return len(box_map[box_id].items) < box_map[box_id].capacity

    # Try to rearrange items in full boxes
    for box in boxes:
        if len(box.items) == box.capacity:  # Full box
            for item in list(box.items):  # Copy list to avoid modifying while iterating
                second_box = box_map[item.second_best_box]
                if can_fit(item.second_best_box):
                    # Move item to its second-best box
                    box.items.remove(item)
                    second_box.add_item(item)
                    break  # Re-check the box after any change to avoid infinite loops

    # Re-check unplaced items
    unplaced_items = []
    for item in items:
        if item not in [i for b in boxes for i in b.items]:  # Check if unplaced
            best_box = box_map[item.best_box]
            second_best_box = box_map[item.second_best_box]
            if can_fit(item.best_box):
                best_box.add_item(item)
            elif can_fit(item.second_best_box):
                second_best_box.add_item(item)
            else:
                unplaced_items.append(item)

    return unplaced_items


# Example Usage
items = [Item(1, 'A', 'B'), Item(2, 'A', 'C'), Item(3, 'B', 'C'), Item(4, 'A', 'B'), Item(5, 'B', 'C'),  Item(6, 'B', 'A'), Item(7, 'C', 'B')]
boxes = [Box('A', 2), Box('B', 2), Box('C', 3)]

unplaced = sort_items_to_boxes(items, boxes)

for box in boxes:
    print(f"Box {box.id} contains items: {[item.id for item in box.items]}")

print(f"Unplaced items: {[item.id for item in unplaced]}")

unplaced = optimize_placements(unplaced, boxes)
for box in boxes:
    print(f"Box {box.id} contains items: {[item.id for item in box.items]}")

print(f"Unplaced items: {[item.id for item in unplaced]}")

