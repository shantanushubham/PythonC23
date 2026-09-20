# Inheritance is a pre-requisite


from abc import ABC, abstractmethod
from typing import override

# Abstract Class
# 1. It is a class. So it will nehave just like a class.
# 2. We cannot create an object of abstract class.
# 3. An abstract class can contain non-abstract as well as abstract methods/functions.
# 4. An abstract function is the function that is mandatory to be overriden in the child/decendent of the abstract class.
# 5. An abstract function has no function body. It only contains arguments.

# Why?
# It is done to protect the internal implementation of something.



class Engine(ABC):

    def test(self):
        print("Test")

    @abstractmethod # It has meaning
    def start(self):
        pass
        

    @abstractmethod
    def stop(self):
        pass
        


class PEngine(Engine):

    @override
    def start(self):
        print("Starting Petrol Engine")
        # Some code that has all the complexities of starting petrol engine
        print("Petrol Engine Started")

    @override
    def stop(self):
        print("Stopping Petrol Engine")
        # Some code that has all the complexities of stopping petrol engine
        print("Petrol Engine Stopped")

class EEngine(Engine):

    @override
    def start(self):
        print("Starting Electric Engine")
        # Some code that has all the complexities of starting electric engine
        print("Electric Engine Started")

    @override
    def stop(self):
        print("Stopping Electric Engine")
        # Some code that has all the complexities of stopping electric engine
        print("Electric Engine Stopped")


class Windsor:

    def __init__(self) -> None:
        self.engine = EEngine()

    def start_car(self):
        self.engine.start()

    def stop_car(self):
        self.engine.stop()

class Slavia:

    def __init__(self) -> None:
        self.engine = PEngine()

    def start_car(self):
        self.engine.start()

    def stop_car(self):
        self.engine.stop()


# windor_obj = Windsor()
# windor_obj.start_car()
# windor_obj.stop_car()

# print("***********")
# slavia_obj = Slavia()
# slavia_obj.start_car()
# slavia_obj.stop_car()
# slavia_obj.engine.test()

# print("**************")
# e = Engine()
# e.start()



class Nexon:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def start_car(self):
        self.engine.start()

    def stop_car(self):
        self.engine.stop()


nexon_e_obj = Nexon(EEngine())
nexon_p_obj = Nexon(PEngine())

nexon_e_obj.start_car()
nexon_p_obj.start_car()

