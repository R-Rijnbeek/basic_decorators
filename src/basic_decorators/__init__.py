# -*- coding: utf-8 -*-
"""
basic_decorators: Repository with usefull decorator methods
"""
__author__  = "Robert Rijnbeek"
__email__   = "robert270384@gmail.com"
__version__ = "1.0.0"

# ======== IMPORTS ===========

from time import time 
import json
from functools import wraps

# ======== DECORATORS ========

def execution_timer(func):
    def timer(*args, **kwargs):
        TIME = time()
        res =func(*args, **kwargs)
        timer.time +=time()-TIME
    timer.time = 0
    return timer

def function_counter(func):
    @wraps(func)
    def counter(*args, **kwargs):
        #print(args)
        res =func(*args, **kwargs)
        counter.count +=1
    counter.count = 0
    return counter



def statistic(debug=True):
    if debug :
        def stat(func):
            def function_wrapper(*args, **kwargs):
                TIME = time()
                res =func(*args, **kwargs)
                function_wrapper.info["total_execution_time"] += time() - TIME 
                function_wrapper.info["execution_count"] +=1
                function_wrapper.info["average_execution_time"] = function_wrapper.info["total_execution_time"]/function_wrapper.info["execution_count"]
            function_wrapper.info = {"total_execution_time":0,"execution_count":0,"average_execution_time":None}
            return function_wrapper
        return stat
    else:
        def stat(func):
            func.info = {}
            return func
        return stat

def statistic_logger(debug=True):
    if debug :  
        def stat(f):
            @wraps(f)
            def function_wrapper(*args, **kwargs):
                function_name = f.__name__
                TIME = time()
                if function_name in statistic_logger.info:
                    res =f(*args, **kwargs)
                    new_dict = statistic_logger.info[function_name]
                else:
                    res =f(*args, **kwargs)
                    new_dict = {"total_execution_time":0,"execution_count":0,"average_execution_time":None}
                new_dict["total_execution_time"] += time() - TIME 
                new_dict["execution_count"] +=1
                new_dict["average_execution_time"] = new_dict["total_execution_time"]/new_dict["execution_count"]
                statistic_logger.info[function_name]=new_dict
            statistic_logger.info = {}
            return function_wrapper
        statistic_logger.info =  {}
        return stat
    else:
        def stat(f):
            return f
        statistic_logger.info =  {}
        return stat    


def new_logger(debug=True):
    if debug :  
        def logger_expr(f):
            def function_wrapper(*args, **kwargs):
                try:
                    responce = f(*args, **kwargs)
                    new_logger.info.append({"metodo": str(f.__name__ ),"type":str(f.__class__),"path":str(f.__code__.co_filename), "arg": list(map(lambda x:str(x),args)) , "kwargs": kwargs , "output": str(responce),"status":True})
                    return responce
                except:
                    new_logger.info.append({"metodo": f.__name__ ,"type":str(f.__class__),"path":f.__code__.co_filename, "arg": list(map(lambda x:str(x),args)) , "kwargs": kwargs , "output": None,"status":False})
                    #raise ValueError("error executing function")
            return function_wrapper
        new_logger.info = []
        return logger_expr
    else:
        def logger_expr(f):
            return f
        new_logger.info = []
        return logger_expr    


def logger(debug=True):
    if debug :  
        def logger_expr(f):
            def function_wrapper(*args, **kwargs):
                #try:
                    responce = f(*args, **kwargs)
                    print({"metodo": f.__name__ ,"type":str(f.__class__),"path":f.__code__.co_filename, "arg": str(args) , "kwargs": str(kwargs) , "output": str(responce),"status":True})
                    return responce
                #except:
                    #print({"metodo": f.__name__ ,"type":f.__class__,"path":f.__code__.co_filename, "arg": str(args) , "kwargs": str(kwargs) , "output": None,"status":False})
            return function_wrapper
        return logger_expr
    else:
        def logger_expr(f):
            return f
        return logger_expr
        
def argument_check(*types_args,**types_kwargs):
    """
    INFORMATION: Standard decorator with arguments that is used to verify the agument (arg) or opttion arguments (kwargs) 
                 of linked function. If the decorator see an not valid argument or kwarg in the funcion. 
                 There will be generate an exception with the explanation with the argument that is not correct.
    INPUT: 
        - *types_args: Tuple of arguments where eatch argument can will be a a type (simple object type) or types of 
                       object types (when you define a tuple of objects). Or if it is defined as an list. Those values of the list 
                       are the option of the values thay those arguments can will be.
        - **types_kwargs: dict of kwargs where eatch argument can will be a a type (simple object type) or types of object types 
                          (when you define a tuple of objects). Or if it is defined as an list for a key of a dict. The keyvalue of a
                          dict must be in the defined list liked to that veyvalue.
    OUTPUT:
        - ERROR: EXECUTION OF THE LINKED FUNCTION
        - NO ERROR: A DEFINED EXCEPTION

    """
    def check_accepts(f):
        def function_wrapper(*args, **kwargs):
            assert len(args) is len(types_args), f"In function '{f.__name__}{args}' and option values: {kwargs}, lenght of argumnets {args} is not the same as types_args {types_args}"
            for (arg, type_arg) in zip(args, types_args):
                if isinstance(type_arg,list):
                    assert arg in type_arg, f"In function '{f.__name__}{args}' and option values: {kwargs}, argument {arg} is not in list {type_arg}" 
                else:
                    assert isinstance(arg, type_arg), f"In function '{f.__name__}{args}' and option values: {kwargs}, arg {arg} does not match {type_arg}" 
            for kwarg,value in kwargs.items():
                assert kwarg in types_kwargs , f"In function '{f.__name__}{args}' and option values: {kwargs}, the kwarg ('{kwarg}':{value}) is not a valid option value" 
                espected_format = types_kwargs[kwarg]
                if isinstance(espected_format,list): 
                    assert value in espected_format, f"In function '{f.__name__}{args}' and option values: {kwargs}, the kwarg value ('{kwarg}':{value}) is not in list {espected_format}" 
                else:
                    assert isinstance(value, espected_format), f"In function '{f.__name__}{args}' and option values: {kwargs}, kwarg value ('{kwarg}':{value}) does not match with {espected_format}" 
            return f(*args, **kwargs)
        function_wrapper.__name__ = f.__name__
        return function_wrapper
    return check_accepts 

def type_arguments_for_all(TYPE,**types_kwargs):
    def check_accepts(f):
        def function_wrapper(*args, **kwargs):
            for arg in args:
                assert isinstance(arg, TYPE), "arg %r does not match %s" % (arg,TYPE)
            for kwarg,value in kwargs.items():
                assert kwarg in types_kwargs , f"In function '{f.__name__}{args}' and option values: {kwargs}, the kwarg ('{kwarg}':{value}) is not a valid option value" 
                espected_format = types_kwargs[kwarg]
                if isinstance(espected_format,list): 
                    assert value in espected_format, f"In function '{f.__name__}{args}' and option values: {kwargs}, the kwarg value ('{kwarg}':{value}) is not in list {espected_format}" 
                else:
                    assert isinstance(value, espected_format), f"In function '{f.__name__}{args}' and option values: {kwargs}, kwarg value ('{kwarg}':{value}) does not match with {espected_format}"
            return f(*args, **kwargs)
        function_wrapper.__name__ = f.__name__
        return function_wrapper
    return check_accepts



if __name__ == "__main__":

    pass

