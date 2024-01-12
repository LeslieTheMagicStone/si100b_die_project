from EventSystem import *


# post an event to tell the scene to add it to the object list, and return the object
def generate(obj):
    EventSystem.fire_generate_event(obj)
    return obj
