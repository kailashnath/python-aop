from functools import wraps
from inspect import isfunction, ismethod

ENABLE_AOP = True


BEFORE = {}
AFTER = {}


def uid(func):
    return id(func.func_code)


def register(coll,joinPoint, *advices):
    act_func = getattr(joinPoint, '__aop_func__', None)

    if not act_func:
        raise TypeError("The %s is not watchable" % joinPoint)

    jid = uid(act_func)

    if jid in coll:
        coll[jid] += advices
    else:
        coll[jid] = advices


def before(joinPoint, *advices):
    global BEFORE
    register(BEFORE, joinPoint, *advices)


def after(joinPoint, *advices):
    global AFTER
    register(AFTER, joinPoint, *advices)


def around(joinPoint, b, a):
    global BEFORE, AFTER
    before(joinPoint, b)
    after(joinPoint, a)


def call(fs, *args, **kwargs):
    if ENABLE_AOP:
        for f in fs:
            f(*args, **kwargs)


def watchable(func):
    id = uid(func)

    @wraps(func)
    def wrap(*args, **kwargs):
        befores = BEFORE.get(id, None)
        if befores:
            call(befores, *args, **kwargs)

        result = func(*args, **kwargs)

        afters = AFTER.get(id, None)
        if afters:
            kwargs['result'] = result
            call(afters, *args, **kwargs)

        return result

    wrap.__aop_func__ = func
    return wrap

