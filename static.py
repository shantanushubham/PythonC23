class Animal:

    type = "Dog" # Assume it is class-level member

    def __init__(self, name):
        self.name = name


obj = Animal("Jimmy")
print(obj.type) # Uses static
print(Animal.type) # Uses static

Animal.type = "Cat" # Changes static
print(Animal.type, obj.type) # Uses static in both cases

obj.type = "Parrot" # creates a new non-static 'type' for object
print(Animal.type, obj.type) # Uses static and non-static respectively

Animal.type = "Rat" # Changes static
print(Animal.type, obj.type) # Uses static in both cases

obj.color = "Brown" # creates a new non-static 'color' for object
print(obj.color) # uses non-static member 'color'

Animal.breed = "German Shephard"

# []["Cat"][][][M1, M2, M3][][][][]["Jimmy"]["Parrot"]][][][][][][][][]["Brown"]
#     type         obj            M1        M2                         M3


"""Members of the class
1. Whatever we write inside the class, it is a member of the class. This usually includes the following:
- Variables
- Functions

Members also also be classified in two ways:
1. Members that are class-level (aka static) - to access this kind of member, we don't need an object, but can be used with an object
2. Members that are object-level (aka non-static) - to access this kind of member, an object is necessary!
"""