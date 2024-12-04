# Unsupported Grammar Cases

This file outlines the features and functionalities of the Python grammar that are not supported by this transpiler due to time and complexity constraints. Below you will find detailed descriptions of each unsupported case, along with example code snippets demonstrating the issue.

---

## 1. Comma chained assignations

### Description:

This case refers to Python's ability to have multiple assignations separated by a comma in a single line. This feature has been excluded due to potential ambiguity and the increased complexity it introduces when parsing, particularly in relation to other more commonly used assignment patterns. As a result, any attempt to use this syntax will not be recognized by the parser, leading to an error and halting the parsing process.

### Examples:

#### Unsupported cases:

```python
# Unsupported chained assignation
a = 5, b = 6, c = 7
```

```python
# Unsupported chained assignation
a = 5,7,8, b = "hello"
```

```python
# Unsupported chained assignation
a, b, c = d, f, z = True, epsilon = None
```

#### Supported cases:

```python
# Supported chained assignation
a = b = c = 7
```

```python
# Supported chained assignation
a, b, c = "hello", "world", 8
```

```python
# Supported chained assignation
a, b, c = (3, 2, {3:"a"})
```

## 2. Dynamic attribute addition to objects

### Description:

This case refers to Python's ability to add new attributes to an object after it has been instantiated from a predefined class. In Python, this can be done by assigning values to attributes that were not originally defined within the class. This feature has been excluded from the transpiler due to the complexity it introduces in tracking and validating dynamically created attributes during parsing. While the syntax will be recognized by the parser, the absence of pre-declared attributes will result in a semantic error later in the process.

### Examples:

#### Unsupported cases:

```python
# Unsupported dynamic addition of attributes
class dog():
    def __init__(self, mood, color):
        self.mood = mood
        self.color = color

my_dog = dog("happy", "brown")
my_dog.breed = "German shepherd"
```

#### Supported cases:

```python
# Supported alternative to dynamic addition of attributes
class dog():
    def __init__(self, mood, color):
        self.mood = mood
        self.color = color
        self.breed = None

my_dog = dog("happy", "brown")
my_dog.breed = "German shepherd"
```

## 3. Immediate function return access

### Description:

This case refers to accessing methods, attributes, or performing indexation directly on the return value of a function immediately after the function call. This feature has been excluded from the transpiler due to the complexity involved in tracking and validating whether the return type from a given function supports the intended operation. As a result, this syntax will not be recognized by the parser, leading to an error and terminating the parsing process.

### Examples:

#### Unsupported cases:

```python
# Unsupported inmidiate function return access
class dog():
    def __init__(self, mood, color):
        self.mood = mood
        self.color = color

my_dogs_color = dog("happy", "brown").color
```

```python
# Unsupported inmidiate function return access
def create_set():
    my_set = {"something"}
    return my_set

create_set().add("something else")
```

```python
# Unsupported inmidiate function return access
def create_list():
    my_list = [1, 2, 3, 4]
    return my_list

print(create_list()[-1])
```

#### Supported cases:

```python
# Supported alternative to immediate function return access
class dog():
    def __init__(self, mood, color):
        self.mood = mood
        self.color = color

my_dog = dog("happy", "brown")
my_dogs_color = my_dog.color
```

```python
# Supported alternative to inmidiate function return access
def create_set():
    my_set = {"something"}
    return my_set

my_new_set = create_set()
my_new_set.add("something else")
```

```python
# Supported alternative to inmidiate function return access
def create_list():
    my_list = [1, 2, 3, 4]
    return my_list

my_new_list = create_list()
print(my_new_list[-1])
```

## 4. Argument specification

### Description:

This case refers to Python's ability to specify the value of function arguments by name during a function call, using keyword arguments. This feature has been excluded from the transpiler due to the complexity and potential ambiguity it introduces, particularly when handling assignments as parameters and verifying the existence and correctness of the named arguments. As a result, this syntax will not be recognized by the parser, leading to undefined behavior. It may cause a parsing error and terminate the process or be misinterpreted as an assignment, leading to unexpected results.

### Examples:

#### Unsupported cases:

```python
# Unsupported argument specification
def my_function(param1, param2, param3):
    return param1 * param2 + param3

print(my_function(param2=2, param1=1, param3=3))
```

```python
# Unsupported argument specification
def my_function(param1, param2, param3):
    return param1 * param2 + param3

my_value = my_function(param2=2)
```

#### Supported cases:

```python
# Supported alternative to argument specification
def my_function(param1, param2, param3):
    return param1 * param2 + param3

print(my_function(1, 2, 3))
```

```python
# Supported alternative to argument specification
def my_function(param1, param2, param3):
    return param1 * param2 + param3

my_value = my_function(None, 2)
```

## 5. Global and local variable differentiation

### Description:

This case refers to Python's ability to differentiate between local and global variables that share the same name, using the "global" keyword to specify when a global variable should be used within a local context. This feature has been excluded from the transpiler due to the complexity involved in tracking, validating, and managing multiple variables with the same name across different scopes. As a result, variables with the same name are treated as a single entity in the transpiler. To prevent the use of this feature, the "global" keyword has not been implemented. Attempts to use it will not be recognized by the lexer, resulting in an error and terminating the lexing process.

### Examples:

#### Unsupported cases:

```python
# Unsupported global and local variable differentiation
x = 4
def my_local_function():
    x = 7
    return x

def my_global_function():
    global x
    return x

print(my_local_function() - my_global_function())
```

```python
# Unsupported global and local variable differentiation
x = 4
def change_local():
    x = 7

def change_global():
    global x = 7

print(x)
change_local()
print(x)
change_global()
print(x)
```

#### Supported cases:

```python
# Supported alternative to global and local variable differentiation
x = 4
def my_local_function():
    x_1 = 7
    return x_1

def my_global_function():
    return x

print(my_local_function() - my_global_function())
```

```python
# Supported alternative to global and local variable differentiation
x = 4
def change_local():
    x_1 = 7

def change_global():
    x = 7

print(x)
change_local()
print(x)
change_global()
print(x)
```

## 6. Type hinting value enforcement

### Description:

This case refers to the desired behavior of enforcing that variables conform to their type hints, preventing assignments of values that do not match the specified type. While Python does not enforce this, it was considered for the transpiler. However, due to the complexity of validating types across expressions, conditions, and function calls, this feature was excluded. As a result, type hints will be recognized but not enforced, allowing variables to be assigned values of any type, regardless of the hint.

### Examples:

#### Supported cases:

```python
# Supported usage of type hinting without enforcement
def my_function(my_string : str, my_int : int):
    print(my_string + my_int)

my_function([True, False, True], (None, None))
```

```python
# Supported usage of type hinting without enforcement
my_fake_list : list[str] = True
my_fake_bool : bool = []

my_fake_bool = my_fake_list
```

## 7. Nested type hints

### Description:

This case refers to Python’s ability to specify type hints for nested containers, where a container holds other containers with their own type hints. While the transpiler supports type hints for the outermost container, it does not allow hinting the types of containers nested within it. This restriction was introduced due to the complexity and ambiguity that arise when parsing multiple layers of type hints. As a result, attempts to provide type hints for nested containers will not be recognized by the parser, leading to an error and terminating the parsing process.

### Examples:

#### Unsupported cases:

```python
# Unsupported nested type hints
def my_function(param1 : list[list[int], int | bool], param2 : dict[str, set[None]]):
    return len(param1) + len(param2)
```

```python
# Unsupported nested type hints
x : list[tuple[set[list[int]]]] = [({[5,6,7]})]
```

#### Supported cases:

```python
# Supported alternative to nested type hints
def my_function(param1 : list[list, int | bool], param2 : dict[str, set]):
    return len(param1) + len(param2)
```

```python
# Supported alternative to nested type hints
x : list[tuple] = [({[5,6,7]})]
```

## 8. Limited support for the `chr()` function  

### Description:  
This case refers to Python's `chr()` function, which returns the character associated with a given Unicode code point. While this functionality is supported for ASCII values (0–127), handling characters beyond this range presents challenges due to the complexity of managing Unicode in C++. As a result, using `chr()` with non-ASCII values will result in incorrect or faulty characters.  

### Examples:  

#### Unsupported cases:  

```python  
# Unsupported use of chr with non-ASCII values  
print(chr(128))  # Non-ASCII  
print(chr(10000))  
```

```python
# Unsupported use of chr with Unicode code points  
unicode_char = chr(0x1F600)  # 😀 (Unicode emoji)  
print(unicode_char)  
```

#### Supported cases:

```python  
# Supported use of chr with ASCII values  
print(chr(65))  # A  
print(chr(97))  # a  
```

```python
# Supported ASCII range examples  
for i in range(32, 127):  
    print(chr(i), end=" ")  # Printable ASCII characters  
```

## 9. Unsupported use of `super()` and custom class definitions  

### Description:  
This case refers to the use of the `super()` function and the definition of custom classes along with their methods in Python. While the syntax will be recognized by both the lexer and parser, the code generator does not produce output for these constructs. As a result, using `super()` or defining custom classes will lead to undefined behavior. This limitation is due to time constraints in the implementation.  

### Examples:  

#### Unsupported cases:  

```python  
# Unsupported use of super()  
class Parent:  
    def greet(self):  
        print("Hello from Parent")  

class Child(Parent):  
    def greet(self):  
        super().greet()  
        print("Hello from Child")  

child_instance = Child()  
child_instance.greet()  
```

```python  
# Unsupported custom class definition  
class CustomClass:  
    def __init__(self, value):  
        self.value = value  

    def display_value(self):  
        print(f"Value: {self.value}")  

obj = CustomClass(10)  
obj.display_value()  
```

## 10. Unsupported direct calls to dunder methods  

### Description:  
This case refers to directly calling special methods (dunder methods) in Python, such as `__name__` or `__method__`, using dot notation (e.g., `object.__method__`). While these methods often correspond to specific operator overloads or intrinsic behaviors in Python, direct calls to them are not supported by the transpiler. Although the lexer, parser, and code generator will recognize such calls, they are not implemented, leading to compilation errors in C++. The object’s behavior will still function correctly when triggered by the corresponding operator or intrinsic behavior, but explicit method calls will not compile. This limitation is due to time constraints in the implementation.  

### Examples:  

#### Unsupported cases:  

```python  
# Unsupported direct call to dunder method  
class CustomClass:  
    def __str__(self):  
        return "CustomClass instance"  

obj = CustomClass()  
print(obj.__str__())  
```

```python
# Unsupported direct call to dunder method  
my_list = [1, 2, 3]  
print(my_list.__len__())  
```

```python
# Unsupported direct call to dunder method  
class WithAdd:  
    def __add__(self, other):  
        return "Adding"  

obj = WithAdd()  
print(obj.__add__(5))   
```

## 11. Limited support for the `dict()` function  

### Description:  
This case refers to the use of the `dict()` function for constructing dictionaries in Python. The transpiler only supports calling `dict()` without any parameters to create an empty dictionary. Using `dict()` with any arguments, such as key-value pairs or iterable inputs, is not supported. Such usage will either cause the parser to fail or result in compilation errors. However, dictionaries can still be created directly with key-value pairs using curly braces `{}`. This limitation is due to time constraints in the implementation.  

### Examples:  

#### Unsupported cases:  

```python  
# Unsupported use of dict() with key-value pairs  
my_dict = dict(a=1, b=2)  
```

```python  
# Unsupported use of dict() with iterable input  
my_dict = dict([('a', 1), ('b', 2)])  
```

```python  
# Unsupported use of dict() with keyword arguments  
my_dict = dict(zip(["a", "b"], [1, 2]))  
```

#### Supported cases:

```python  
# Supported use of dict() to create an empty dictionary  
empty_dict = dict()
```

```python  
# Supported direct creation of dictionaries with key-value pairs  
my_dict = {"a": 1, "b": 2, "c": 3}
```

## 12. Unsupported reassignment of variables to a different type  

### Description:  
This case refers to the inability to reassign a variable to a value of a different type after it has been initially declared with a specific type. While Python allows dynamic typing, the transpiler does not support this behavior due to the complexity of implementing type flexibility in C++ while maintaining the usability of variables. As a result, attempting to reassign a variable to a value of a different type will cause an error during compilation.  

### Examples:  

#### Unsupported cases:  

```python  
# Unsupported reassignment to a different type  
x = 10  # Initial type is int  
x = "Hello"  # Reassigning to a string (different type)  
```

```python  
# Unsupported reassignment to a different type  
my_var = [1, 2, 3]  # Initial type is list  
my_var = 42  # Reassigning to an int (different type)  
```

```python  
# Unsupported reassignment to a different type  
value = 3.14  # Initial type is float  
value = True  # Reassigning to a boolean (different type)  
```

#### Supported cases:

```python  
# Supported reassignment with the same type  
x = 10  # Initial type is int  
x = 20  # Reassigning with the same type  
```

```python  
# Supported reassignment with the same type  
my_var = [1, 2, 3]  # Initial type is list  
my_var = [4, 5, 6]  # Reassigning with the same type  
```

## 13. Unsupported usage of extremely large numbers  

### Description:  
This case refers to the limitation in handling extremely large numbers. While Python supports arbitrarily large integers and floating-point numbers, C++ has fixed-size number types. As a result, numbers beyond the supported range will cause compilation errors, overflow, or undefined behavior. The transpiler does not handle these cases due to the complexity of implementing support for such large numbers in C++, and the minimal reward from doing so. To avoid errors, numbers should not exceed 2147483647 and -2147483647 for integers, and should stay within the range of -1.7976931348623157 × 10^308 to 1.7976931348623157 × 10^308 for doubles.  

### Examples:  

#### Unsupported cases:  

```python  
# Unsupported extremely large integer  
large_num = 2147483648  # Beyond supported range for int  
```

```python  
# Unsupported extremely small integer  
small_num = -2147483648  # Below supported range for int   
```

```python  
# Unsupported large floating-point number  
large_float = 1.8e308  # Exceeds the maximum range for double  
```

```python  
# Unsupported small floating-point number  
small_float = -1.8e308  # Below the minimum range for double  
```

#### Supported cases:  

```python  
# Supported integer within the valid range  
valid_int = 2147483647  # Maximum supported integer  
```

```python  
# Supported integer within the valid range  
valid_int = -2147483647  # Minimum supported integer  
```

```python  
# Supported floating-point number within the valid range  
valid_float = 1.7976931348623157e308  # Maximum supported double   
```

```python  
# Supported floating-point number within the valid range  
valid_float = -1.7976931348623157e308  # Minimum supported double  
```

