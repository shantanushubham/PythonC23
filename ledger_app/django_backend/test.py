class Test:

    # instance is the OLD STATE OF THE OBJECT.

    def __init__(self, name, age, instance=None, **kwargs):
        self.name = name
        self.age = age
        self.instance = instance
        self.extra = kwargs
        # I am creating a dictionary which contains the kwargs and the name and age passed to the constructor.
        data = dict(**kwargs, name=name, age=age)
        self.validated_data = self.validate(data)

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"

    # returns validated object
    def validate(self, attrs):
        print("Validating attributes", attrs)

        # GetOrDefault
        self.name = attrs.get("name", self.name)

        proposed_age = attrs.get("age")

        if proposed_age is not None:
            if proposed_age > 18:
                self.age = proposed_age
            else:
                raise ValueError("Age must be greater than 18")

        return attrs


test = Test(name="John", age=20)
print("Validated Data:", test.validated_data)

test2 = Test(instance=test, **{"name": "Andrew", "age": 27, "city": "New York", "country": "USA"})
print(test2)
print("Validated Data:", test2.validated_data)



# data = {"age": 20}

# print(data.get("name", "Surya"))
