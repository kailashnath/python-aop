import aspects


def _call(func, *args, **kwargs):
    if args:
        if kwargs:
            return func(*args, **kwargs)
        return func(*args)
    return func()


def _around(joinPoint, before=None, after=None):
    def wrap(*args, **kwargs):
        retVal = None
        if before:
            _call(before, *args, **kwargs)

        retVal = yield aspects.proceed(*args, **kwargs)

        if after:
            kwargs['result'] = retVal
            _call(after, *args, **kwargs)
        yield aspects.return_stop(retVal)

    return wrap


def before(joinPoint, advice):
    aspects.with_wrap(_around(joinPoint, before=advice), joinPoint)


def after(joinPoint, advice):
    aspects.with_wrap(_around(joinPoint, after=advice), joinPoint)


def around(joinPoint, before, after):
    aspects.with_wrap(_around(joinPoint, before=before, after=after), joinPoint)

