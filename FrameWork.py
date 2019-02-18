# Building framework for validating assertions
# @Simranjeet Singh Dua
class Contract(object):
    type_=None
    @classmethod
    def check(cls,value):
        assert isinstance(value,cls.type_), f'{value} should be {cls.type_}'

class Typed(Contract):
    @classmethod
    def check(cls,value):
        super().check(value)

class Integer(Typed):
    type_=int

class Float(Typed):
    type_=float

class String(Typed):
    type_=str    

class Positive(Contract):
    @classmethod
    def check(cls,value):
        assert value>0, f'{value} must be greater than zero'
        super().check(value)


class PositiveInteger(Integer,Positive):
    pass

from functools import wraps
from inspect import signature
def checked(func):
    @wraps(func)
    def inside(*args,**kwargs):
        print()
        sign=signature(func)
        sign=sign.bind(*args,**kwargs)
        sign.apply_defaults()
        for var,value in sign.arguments.items():
            if var in func.__annotations__:
                try:
                    if isinstance(value,dict):
                        for val in value.values():
                            func.__annotations__[var].check(val)
                    else:
                        for val in value:
                            func.__annotations__[var].check(val)
                except TypeError:
                    func.__annotations__[var].check(value)
        return func(*args,**kwargs)
    return inside    

@checked
def func(*args:Integer,**kwargs:PositiveInteger):
    print('Hurray!!! successful')
func(1,2.0,3,k=1,f=89)









