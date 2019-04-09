# validator.py
from functools import wraps
from inspect import signature
from itertools import zip_longest


def accepts(**accepted_arg_types):
    def accept_decorator(validate_function):
        @wraps(validate_function)
        def inside(*args, **kwargs):
            if len(accepted_arg_types)==0:
                return validate_function(*args,**kwargs)
            sign = signature(validate_function)
            sign = sign.bind(*args, **kwargs)
            sign.apply_defaults()
            for var, value in sign.arguments.items():
                if var in accepted_arg_types:
                    try:
                        assert isinstance(
                            value, accepted_arg_types[var]), f'{var} must satisfy accepted argument!!!! condition'
                    except TypeError:
                        try:
                            assert type(accepted_arg_types[var]) is type(value)
                            it1 = iter(accepted_arg_types[var])
                            it2 = iter(value)
                            print('here', it1, it2)
                            for type_req, given_var in zip_longest(it1, it2, fillvalue=accepted_arg_types[var][-1]):
                                print(given_var, type_req)
                                assert isinstance(
                                    given_var, type_req), f'{var} must satisfy accepted argument condition'
                        except TypeError:
                            raise Exception(
                                f'{var} must satisfy accepted argument condition')
            return validate_function(*args, **kwargs)
        return inside
    return accept_decorator


def returns(*accepted_return_type_tuple):
    def return_decorator(validate_function):
        @wraps(validate_function)
        def decorator_wrapper(*args, **kwargs):
            return_value = validate_function(*args, **kwargs)
            if len(accepted_return_type_tuple) == 0:
                return return_value
            if type(return_value) is not tuple:#means single value returned by function
                return_value=(return_value,)
            for value,required_type in zip(return_value,accepted_return_type_tuple):
                    try:
                        assert isinstance(
                            value, required_type), f'{var} must satisfy accepted argument!!!! condition'
                    except TypeError:
                        try:
                            print(required_type,type(value))
                            assert type(required_type) is type(value)
                            it1 = iter(required_type)
                            it2 = iter(value)
                            print('here', it1, it2)
                            for type_req, given_var in zip_longest(it1, it2, fillvalue=required_type[-1]):
                                print(given_var, type_req)
                                assert isinstance(
                                    given_var, type_req), f'{var} must satisfy accepted argument condition'
                        except TypeError:
                            raise Exception(
                                f'{var} must satisfy accepted argument condition')
        return decorator_wrapper
    return return_decorator


@accepts(c=[int, ], d=[int, ])
@returns([int, ])
def silly(c, d):
    return c+d


silly([2, ], [3, ])
print('yeah that works')
