# passing all but with 
a = 3
a += a + (2 // (6 + 7))
[3, 2][1] += (3, 2)
a = 3
a += a + (2 // (6 + 7))

# More examples of augmented assignments
b = 5
b -= 2
c = 4
c *= 3
d = 10
d /= 2
e = 7
e //= 3
f = 8
f %= 5
g = 2
g **= 3
h = 6
h &= 3
i = 5
i |= 2
j = 7
j ^= 3
k = 4
k <<= 1
l = 8
l >>= 2

# Complex augmented assignments
m = [1, 2, 3]
m[1] += 4
n = {"key": 10}
n["key"] -= 3
o = (1, 2, 3)
p = 5
p += 2 * 3
q = 10
q /= 2 + 3
#[3, 2][2] += (3, 2)
a += len(m) + len(m)**3