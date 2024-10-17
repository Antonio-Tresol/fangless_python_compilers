# Integer with list
a: int = 5
b: list[int] = [1, 2, 3, 4]

# String with tuple
x: str = "hello"
y: tuple[int, str, float] = (42, "world", 3.14)

# Boolean with set
is_active: bool = True
active_flags: set[bool] = {True, False}

# Dictionary with base types
student_scores: dict[str, int] = {"Alice": 90, "Bob": 85}

# Union for different types
value: int | str = 42
optional_value: int | None = None

# Nested type hinting
numbers: list[list, int] = [[1, 2], [3, 4]]
coordinates: tuple[float, float] = (1.1, 2.2)
a : dict[tuple, int, int, list, list, bool] = {}

# Typed assignment using multiple types
data: tuple[int, str] = (100, "test")