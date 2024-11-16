class Perrito:
    def __init__(self, raza: str, color: tuple[int, int, int]) -> None:
        self.raza = raza
        self.color = color

    def camine(self, direccion: int) -> None:
        self.dirrecion = direccion

    def static_whatever() -> None:
        print("hola")


oliver = Perrito("dalmata", (1, 1, 1))