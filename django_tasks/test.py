class Building:

    def __init__(self, name, height):
        self.name = name
        self.height = height


def make(class_name):
    class_obj = class_name("Empire State Building", 102)
    building = Building("Empire State Building", 102)
    return class_obj

building = make(Building)
print(building)