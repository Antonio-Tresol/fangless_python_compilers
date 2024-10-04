# passing all
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
h = 8
i = 9
j = 10
a = j

list = [a,b,c,d,e,f,g,h,i,j,]

a = b = c = 3

if 5:
    a = b = c = d = 3

b = 7

g = [1, 2, 3]
if a in g:
    g = i

if a in 7:
    g = a*b*c*b

x = y = [1, 2, 3]
# a, b = c, d = (1, 2, 3) 
# a, b = b, a
a = b = c = [1, 2, 3]
a[0] = 42
a = "Hello" + (True and " World")
a = 5
a = a + a
a[1:3] = [9, 8]


[1,4,5][1:"a"] = 9
(1,4,)[1] = 4
{5:5, 8:5}[6] = 5
6[7] = 9

None[None] = None

a = None or 5
