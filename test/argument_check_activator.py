import basic_decorators
from basic_decorators import argument_check



basic_decorators.ARGUMENT_CHECK_ACTIVE = False

@argument_check(int, int)
def plus(a,b):
    return a+b

print(plus(1,5.))