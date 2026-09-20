# Poly - Many
# Morph - Form


class Test:

    def add(self, a, b, c=None):
        if c is None:
            return a + b
        return a + b + c

obj = Test()
print(obj.add(5, 6))
print(obj.add(10, 20, 30))

print(10+20)
print("AirTribe"+"Python")