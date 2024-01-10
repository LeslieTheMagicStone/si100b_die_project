from Settings import *
from EventSystem import *
from Projectiles import *

class Generator:
    # Genrate and return the object, and post an event to tell the scene
    @classmethod
    def generate(cls,type:GeneratableType, *args):
        obj = None

        if type == GeneratableType.BULLET:
            obj = Bullet(args)

        EventSystem.fire_generate_event(obj)
        return obj