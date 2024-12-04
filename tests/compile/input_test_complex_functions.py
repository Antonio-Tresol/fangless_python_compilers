
def function1():
    if True:
        if 5:
            x = 0
            while (x <= 8):
                if x:
                    print(x)
                x = x + 1
            return 1
        else:
            return 2
        
    elif True:
        for z, y in enumerate(range(18, 25, 2)):
            if z and y:
                function3()
    else:
        function4()
    
    return 3

def function2():
    if True and False:
        if 0:
            return False
            function2()
        else:
            function3()
            w = 7
            while w:
                function2()
                break
            return False
        return True
    elif False or True:
        function3()
        if True:
            return False
        return True
    else:
        return True

def function3():
    print("function 3 called")

def function4():
    for w in tuple([1,5,7,8]):
        function2()
    return None


function1()
function2()
function3()
function4()