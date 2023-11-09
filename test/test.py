from basic_decorators import new_logger, statistic,statistic_logger, type_arguments_for_all,function_counter, argument_check

import json


@new_logger(debug = True)
@statistic_logger(debug = True)
@type_arguments_for_all(int,option1=int)
def plusd(*args,option1 = 1):
    sumar = 0
    for arg in args:
        sumar += arg 
    return sumar


@function_counter
@new_logger(debug = True)
@statistic_logger(debug = True)
@argument_check(int,int,int,int,option1=int,option2 = float)
def plus(x,y,z,z1,option1 = 1, option2 = 2.):
    return x+y

try:
    for i in range(1000):
        plusd(1,2,3,4,option1 = 2)
        plus(3,2,6,7)
except Exception as exc:
    print(f"{exc}")


print(statistic_logger.info)
print(new_logger.info)

print(json.dumps(new_logger.info,indent=4))
print(json.dumps(statistic_logger.info,indent=4))


"""
try:
    for i in range(1000):
        plus(1,2,4,4,option1=5)
        print(plus.time)
        print(plus.count)
except Exception as exc:
    print(f"{exc}")
"""

"""
def for_all_methods(decorator):
    def decorate(cls):
        for name, member in vars(cls).items(): # there's propably a better way to do this
            if isinstance(member, (types.FunctionType, types.BuiltinFunctionType)):
                setattr(cls, name, decorator(member))
                continue
            if isinstance(member, (classmethod, staticmethod)):
                inner_func = member.__func__
                method_type = type(member)
                decorated = method_type(decorator(inner_func))
                setattr(cls, name, decorated)
                continue

                
        return cls
    return decorate



#@for_all_methods(statistic(debug=True))
#@for_all_methods(logger(debug = True))
@for_all_methods(new_logger(debug = True))
class Clos:

    def __init__(self):
        self.var1 = 10
    
    @staticmethod
    def m1(): 
        return 5

    
    @classmethod
    def m3(cls,Value1):
        return Value1*5

    
    @classmethod
    @argument_check(object,int)
    def m2(cls,x): 
        return x+x + cls.m3(10)

    
    @argument_check(object,int,int,int)
    #@function_counter
    def hola(self, x,y,z):
        return x+y+2*z 


obj = Clos()

try:
    obj.m1()
    obj.m2(5)
    #print(obj.m2.info)
    obj.hola(5,5,6)
    print(new_logger.info)
    #print(obj.hola.count)
except Exception as exc:
    print(exc)
#obj.m1()
#obj.m3(3)


#print(json.dumps(new_logger.info,indent=4))


try:
    obj.hola(1,2,3)
except Exception as exc:
    print(exc)


Clos.m2(5)
Clos.m1()
Clos.m3(3)
"""