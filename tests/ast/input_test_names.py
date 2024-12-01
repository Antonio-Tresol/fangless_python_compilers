# a = b = c = d = 3
class perro:
    def __init__(self) -> None:
        self.bro = list()
        self.sup = 0


class antonio:
    def __init__(self) -> None:
        self.lalo = perro()

class Joe:
    def __init__(self) -> None:
        self.antonio = antonio()


joseph = Joe()
joseph.antonio.lalo.bro.append(1)
