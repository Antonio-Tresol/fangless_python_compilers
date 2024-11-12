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
        self.tpl = (1, 2, 3)


joseph = 1, 2, 3
joseph = Joe()
joseph.antonio.lalo.bro[0] = 1
joseph.antonio.lalo.sup = 1

a, b, c = joseph.tpl


joseph.antonio.lalo.bro[6:8] = joseph.antonio.lalo.bro[-2:-4]
