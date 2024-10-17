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