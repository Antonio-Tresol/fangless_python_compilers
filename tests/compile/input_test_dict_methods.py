# Demonstrating dictionary methods

# clear
print("clear examples:")
d = {"a": 1, "b": 2, "c": 3}
d.clear()
print(d)  # Outputs: {}
d["new"] = 5
print(d)  # Outputs: {"new": 5}
d.clear()
print(d)  # Outputs: {}

# copy
print("\ncopy examples:")
d = {"a": 1, "b": 2}
d_copy = d.copy()
print(d_copy)  # Outputs: {"a": 1, "b": 2}
d["c"] = 3
print(d)       # Outputs: {"a": 1, "b": 2, "c": 3}
print(d_copy)  # Outputs: {"a": 1, "b": 2} (copy is unaffected)
empty_copy = {}.copy()
print(empty_copy)  # Outputs: {}

# fromkeys
print("\nfromkeys examples:")
keys = ["a", "b", "c"]
default_value = 0
print(dict().fromkeys(keys, default_value))  # Outputs: {'a': 0, 'b': 0, 'c': 0}
print(dict().fromkeys(keys))  # Outputs: {'a': None, 'b': None, 'c': None}
empty_keys = []
print(dict().fromkeys(empty_keys, "value"))  # Outputs: {}

# get
print("\nget examples:")
d = {"a": 1, "b": 2}
print(d.get("a"))  # Outputs: 1
print(d.get("c", 0))  # Outputs: 0 (default value)
print(d.get("c"))  # Outputs: None (default when not specified)
print(d.get("b", "default"))  # Outputs: 2

# items
print("\nitems examples:")
d = {"a": 1, "b": 2}
for key, value in d.items():
    print(key + " : " + value)  # Outputs: "a: 1" and "b: 2"
print(list(d.items()))  # Outputs: [('a', 1), ('b', 2)]

# keys
print("\nkeys examples:")
d = {"a": 1, "b": 2}
print(d.keys())  # Outputs: dict_keys(['a', 'b'])
for key in d.keys():
    print(key)  # Outputs: "a", "b"
print(list(d.keys()))  # Outputs: ['a', 'b']

# pop
print("\npop examples:")
d = {"a": 1, "b": 2}
print(d.pop("a"))  # Outputs: 1
print(d)           # Outputs: {'b': 2}
print(d.pop("b", 0))  # Outputs: 2
print(d)  # Outputs: {}

# popitem
print("\npopitem examples:")
d = {"a": 1, "b": 2}
print(d.popitem())  # Outputs: ('b', 2)
print(d)            # Outputs: {'a': 1}
d["c"] = 3
print(d.popitem())  # Outputs: ('c', 3)
print(d)  # Outputs: {'a': 1}


# setdefault
print("\nsetdefault examples:")
d = {"a": 1}
print(d.setdefault("a", 99))  # Outputs: 1
print(d.setdefault("b", 99))  # Outputs: 99
print(d)  # Outputs: {'a': 1, 'b': 99}
print(d.setdefault("c"))  # Outputs: None
print(d)  # Outputs: {'a': 1, 'b': 99, 'c': None}

# update
print("\nupdate examples:")
d = {"a": 1}
d.update({"b": 2})
print(d)  # Outputs: {'a': 1, 'b': 2}
d.update({"c":3})
print(d)  # Outputs: {'a': 1, 'b': 2, 'c': 3}
d.update([("d", 4)])
print(d)  # Outputs: {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d.update()
print(d)  # Outputs: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# values
print("\nvalues examples:")
d = {"a": 1, "b": 2}
print(d.values())  # Outputs: dict_values([1, 2])
for value in d.values():
    print(value)  # Outputs: 1, 2
print(list(d.values()))  # Outputs: [1, 2]
empty_dict = {}
print(empty_dict.values())  # Outputs: dict_values([])
