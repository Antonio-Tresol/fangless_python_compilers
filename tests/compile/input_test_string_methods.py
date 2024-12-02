print("zfill examples:")
print("42".zfill(5))   # Outputs: "00042"
print("-42".zfill(5))  # Outputs: "-0042"
print("42".zfill(2))   # Outputs: "42" (no padding needed)

# upper
print("\nupper examples:")
print("hello".upper())        # Outputs: "HELLO"
print("Hello World".upper())  # Outputs: "HELLO WORLD"

# title
print("\ntitle examples:")
print("hello world".title())     # Outputs: "Hello World"
print("python is FUN".title())  # Outputs: "Python Is Fun"

# swapcase
print("\nswapcase examples:")
print("Hello World".swapcase())  # Outputs: "hELLO wORLD"
print("PyThOn Is FuN".swapcase())  # Outputs: "pYtHoN iS fUn"

# strip
print("\nstrip examples:")
print("   hello   ".strip())       # Outputs: "hello"
print("###hello###".strip("#"))    # Outputs: "hello"
print("hello".strip("#"))          # Outputs: "hello" (no characters to strip)

# startswith
print("\nstartswith examples:")
print("hello world".startswith("hello"))  # Outputs: True
print("hello world".startswith("world"))  # Outputs: False
print("hello world".startswith("world", 6))  # Outputs: True

# splitlines
print("\nsplitlines examples:")
print("hello\nworld".splitlines())      # Outputs: ['hello', 'world']
print("hello\nworld".splitlines(True))  # Outputs: ['hello\n', 'world']

# split
print("\nsplit examples:")
print("a,b,c".split(","))                 # Outputs: ['a', 'b', 'c']
print("hello world".split())              # Outputs: ['hello', 'world']
print("hello world".split(" ", 1))        # Outputs: ['hello', 'world']

# capitalize
print("capitalize example:")
print("hello world".capitalize())  # Outputs: "Hello world"

# casefold
print("\ncasefold example:")
print("HELLO".casefold())  # Outputs: "hello"

# center
print("\ncenter example:")
print("hello".center(10, "-"))  # Outputs: "--hello---"

# find
print("\nfind example:")
print("hello world".find("world"))  # Outputs: 6

# index
print("\nindex example:")
print("hello world".index("world"))  # Outputs: 6

# isalnum
print("\nisalnum example:")
print("hello123".isalnum())  # Outputs: True
print("hello 123".isalnum())  # Outputs: False

# isalpha
print("\nisalpha example:")
print("hello".isalpha())  # Outputs: True
print("hello123".isalpha())  # Outputs: False

# isascii
print("\nisascii example:")
print("hello".isascii())  # Outputs: True

# isdecimal
print("\nisdecimal example:")
print("123".isdecimal())  # Outputs: True
print("123.45".isdecimal())  # Outputs: False

# isdigit
print("\nisdigit example:")
print("123".isdigit())  # Outputs: True
print("123.45".isdigit())  # Outputs: False

# isidentifier
print("\nisidentifier example:")
print("variable".isidentifier())  # Outputs: True
print("123variable".isidentifier())  # Outputs: False

# islower
print("\nislower example:")
print("hello".islower())  # Outputs: True
print("Hello".islower())  # Outputs: False

# isnumeric
print("\nisnumeric example:")
print("123".isnumeric())  # Outputs: True
print("123.45".isnumeric())  # Outputs: False

# isprintable
print("\nisprintable example:")
print("hello".isprintable())  # Outputs: True
print("hello\nworld".isprintable())  # Outputs: False

# isspace
print("\nisspace example:")
print("   ".isspace())  # Outputs: True
print("hello world".isspace())  # Outputs: False

# isupper
print("\nisupper example:")
print("HELLO".isupper())  # Outputs: True
print("Hello".isupper())  # Outputs: False

# join
print("\njoin example:")
print(", ".join(["apple", "banana", "cherry"]))  # Outputs: "apple, banana, cherry"

# ljust
print("\nljust example:")
print("hello".ljust(10, "-"))  # Outputs: "hello-----"

# lower
print("\nlower example:")
print("HELLO".lower())  # Outputs: "hello"

# lstrip
print("\nlstrip example:")
print("   hello   ".lstrip())  # Outputs: "hello   "
print("###hello###".lstrip("#"))  # Outputs: "hello###"

# partition
print("\npartition example:")
print("hello world".partition(" "))  # Outputs: ('hello', ' ', 'world')

# replace
print("\nreplace example:")
print("hello world".replace("world", "Python"))  # Outputs: "hello Python"

# rfind
print("\nrfind example:")
print("hello world world".rfind("world"))  # Outputs: 12

# rjust
print("\nrjust example:")
print("hello".rjust(10, "-"))  # Outputs: "-----hello"

# rpartition
print("\nrpartition example:")
print("hello world".rpartition(" "))  # Outputs: ('hello', ' ', 'world')

# rsplit
print("\nrsplit example:")
print("a,b,c".rsplit(",", 1))  # Outputs: ['a,b', 'c']

# rstrip
print("\nrstrip example:")
print("   hello   ".rstrip())  # Outputs: "   hello"
print("###hello###".rstrip("#"))  # Outputs: "###hello"
