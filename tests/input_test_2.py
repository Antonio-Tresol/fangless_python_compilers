# This program tests a variety of rules in the FanglessPythonLexer


# Function definition with arithmetic operations and return
def calculate_sum(a, b):
    result = a + b - 3 * (b / 2) % a
    return result


# Conditional logic with boolean values, and comparison
def check_value(x):
    if x == 0:
        return True
    elif x > 0 and x < 100:
        return False
    else:
        return None


# Class definition with method and attribute assignment
class ExampleClass:
    def __init__(self, value):
        self.value = value

    def update_value(self, new_value):
        self.value = new_value


# Loops: while and for
def loop_example(n):
    for i in range(n):
        if i % 2 == 0:
            continue
        else:
            break
    while n > 0:
        n -= 1


# Logical operations with True, False, not, and or
def logical_operations(a, b):
    if not a and b or a:
        return True
    else:
        return False


# Testing punctuation and brackets
def punctuate():
    test_list = [1, 2, 3]
    test_dict = {"key": "value"}
    if (test_list[0] > 0) and {"set_item"} == {"set_item"}:
        print("Punctuation and brackets test passed!")


# Testing indentation and dedentation with pass
def indented_function():
    if True:
        pass
    elif False:
        pass
    else:
        pass


# Testing number literals and strings
def literals():
    number = 123.45
    string = "This is a test string!"
    return number, string


# End of file (endmarker)
