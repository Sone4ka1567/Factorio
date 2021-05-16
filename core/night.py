from maps import Map


def run_night(map_object: Map):
    for cell in map_object.map_objects.values():
        if cell.usable_object:
            cell.usable_object.process()
