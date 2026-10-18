# unlimited positional arguments
def add(*args):
    return_sum = 0
    for n in args:
        return_sum += n
    return return_sum


print(add(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

# unlimited keyword arguments


def calculate(n, **kwargs):
    print(kwargs)
    for key, value in kwargs.items():
        print(key, value)
        print(kwargs["add"])
    n += kwargs["add"]
    n *= kwargs["multiply"]

    print(n)


calculate(n=2, add=3, multiply=5)


class Car:
    def __init__(self, **kwargs):
        self.make = kwargs["make"]
        self.model = kwargs["model"]  # optional - kwargs.get("model")


my_car = Car(make="Nissan", model="GT-R")
print(my_car.model)
