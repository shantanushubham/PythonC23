from typing import override


class Parent:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def my_static_function():
        print("Static")

    def test_function(self):
        print("Inside Parent Class")


class Child(Parent):

    def __init__(self, name, age):
        super().__init__(name) # Calling Parent's Constructor
        self.age = age
        

    def my_function(self) -> str:
        print("Inside Child Class")

    @override # Doesn't do anything. Just good practice
    def test_function(self):
        print("Inside Child Class")
        super().test_function()

c = Child("Akash", 30)
print(c.name)
c.test_function()

# In Python. when we are inside a class and we want to refer to a non-static member of the same class, we use `self`.
# In Python. when we are inside a class and we want to refer to a non-static member of the parent class, we use `super`.