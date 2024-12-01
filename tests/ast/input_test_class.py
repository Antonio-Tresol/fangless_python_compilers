class Animal:
    species_count = 0  # Class variable

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        Animal.species_count += 1

    def make_sound(self) -> str:
        return "Generic dog sound"

    def is_adult(age: int) -> bool:
        return age >= 1


class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str) -> None:
        parent = super()
        parent.__init__(name, age)
        self.breed = breed

    def make_sound(self) -> str:
        return "Woof!"

    def fetch(self, item: str) -> str:
        return self.name + "is fetching " + item


# Test usage
dog = Dog("Rex", 3, "Labrador")
print(dog.make_sound())
print(dog.fetch("ball"))
print(Dog.is_adult(dog.age))