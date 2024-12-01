# Testing iter with a list
print("Testing iter with a list")
# Expected output: 1, 2, 3 (each on a new line)
a = [1, 2, 3]
list_iter = iter(a)
print(list_iter)
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print("")

# Testing iter with a tuple
print("Testing iter with a tuple")
# Expected output: 'a', 'b', 'c' (each on a new line)
b = ('a', 'b', 'c')
tuple_iter = iter(b)
print(next(tuple_iter))
print(next(tuple_iter))
print(next(tuple_iter))
print("")

# Testing iter with a string
print("Testing iter with a string")
# Expected output: 'h', 'e', 'l', 'l', 'o' (each on a new line)
c = "hello"
string_iter = iter(c)
print(next(string_iter))
print(next(string_iter))
print(next(string_iter))
print(next(string_iter))
print(next(string_iter))
print("")

# Testing iter with a set
print("Testing iter with a set")
# Output order may vary: Expected values: 1, 2, 3 (each on a new line)
d = {1, 2, 3}
set_iter = iter(d)
print(next(set_iter))
print(next(set_iter))
print(next(set_iter))
print("")

# Testing iter with a dictionary (iterates over keys)
print("Testing iter with a dictionary")
# Expected output: 'key1', 'key2' (each on a new line)
e = {'key1': 10, 'key2': 20}
dict_iter = iter(e)
print(next(dict_iter))
print(next(dict_iter))
print("")

# Testing iter with a range
print("Testing iter with a range")
# Expected output: 0, 1, 2 (each on a new line)
f = range(3)
range_iter = iter(f)
print(next(range_iter))
print(next(range_iter))
print(next(range_iter))
print("")