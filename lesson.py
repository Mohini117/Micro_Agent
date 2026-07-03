x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()
    print(x)

outer()
print(x)

x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)   # inner has no local x of its own
    inner()

outer()


x = "global"

def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        print(x)
        x = "local"   # this line added
    inner()

outer()

def get_two_numbers():
    return 1, 2

result = get_two_numbers()
print(result)
print(type(result))
b,a = get_two_numbers()
print(a)
print(b)
