import contextlib
import datetime
import sys


class OutStream(object):  # pragma no cover
    """
    This class exisist for easing testing of sys.stdout and doesn't
    need to be tested itself
    """
    def write(self, *args, **kwargs):
        sys.stdout.write(*args, **kwargs)


@contextlib.contextmanager
def Timer(name='', pretty=False):
    """
    A context manager for timing sections of code.
    :type name: str
    :param name: The name you want to give the contextified code
    :type pretty: bool
    :param pretty: When set to true, prints elapsed time in hh:mm:ss.mmmmmm
    Example
    ---------------------------------------------------------------------------
    # this code in a python script
    import time
    from pandashells import Timer
    with Timer('entire script'):
        for nn in range(3):
            with Timer('loop {}'.format(nn + 1)):
                time.sleep(.1 * nn)
    # Will generate the following output on stdout
    #     col1: a string that is easily found with grep
    #     col2: the time in seconds (or in hh:mm:ss if pretty=True)
    #     col3: the value passed to the 'name' argument of Timer

    __time__,2.6e-05,loop 1
    __time__,0.105134,loop 2
    __time__,0.204489,loop 3
    __time__,0.310102,entire script
    ---------------------------------------------------------------------------
    """
    tstart = datetime.datetime.now()
    stream = OutStream()
    yield
    dt = datetime.datetime.now() - tstart
    dt = dt if pretty else dt.total_seconds()
    stream.write('__time__,{},'.format(dt))
    if name:
        stream.write('%s\n' % name)
