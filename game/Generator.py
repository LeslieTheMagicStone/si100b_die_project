from EventSystem import EventSystem


# post an event to tell the scene to add it to the object list, and return the object
def generate(obj, scene=None):
    EventSystem.fire_generate_event(obj, scene)
    return obj
