# This program tests all of the rules in the FanglessPythonLexer


# Function definition with return
def calculate(a, b):
    result = a + b - (b / 2) * a % 5
    return result


# Testing conditionals with logical operators and booleans
def check_value(x):
    if x == 0:
        return True
    elif x > 0 and x < 100 or not False:
        return False
    else:
        return None


# Class definition with methods
class MyClass:
    def __init__(self, value):
        self.value = value

    def update_value(self, new_value):
        if new_value > 0:
            self.value = new_value
        else:
            self.value = 0

    def get_value(self):
        return self.value


# Testing while loop, for loop, and keywords: continue, break
def loop_example(n):
    while n > 0:
        if n % 2 == 0:
            n -= 1
            continue
        else:
            break
    for i in range(10):
        if i == 5:
            break
        else:
            continue


# Testing logical operators with boolean values
def logical_operations(a, b):
    if not a and b or a:
        return True
    else:
        return False


# Testing class method call
obj = MyClass(10)
obj.update_value(15)
result = obj.get_value()


# Testing literals: numbers and strings
def test_literals():
    number = 123.45
    string = "This is a test string!"
    return number, string


# Testing indentation and dedentation
def indented_blocks():
    if True:
        pass  # Testing the 'pass' keyword
    elif False:
        pass
    else:
        pass


# Testing parentheses, brackets, curly braces, and punctuation
def punctuation_test():
    test_list = [1, 2, 3]
    test_dict = {"key": "value"}
    test_tuple = (1, 2, 3)
    if test_list[0] == 1 and test_dict["key"] == "value" and test_tuple[2] == 3:
        print("All punctuation tests passed!")


# Testing assign operator
a = 5
b = 10
a = b + 3


# Testing comparators: ==, <, >, <=, >=
def comparison_test(a, b):
    if a == b:
        return True
    elif a < b:
        return False
    elif a > b:
        return True
    elif a <= b:
        return False
    elif a >= b:
        return True
    else:
        return None


# Testing exclamation (logical not)
def not_test(a):
    if not a:
        return True
    return False


# Testing complex arithmetic
def arithmetic_test(a, b):
    return (a + b) * (b - a) / (a % b)


# Test function call
result = arithmetic_test(10, 20)
