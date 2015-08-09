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
def Timer(name=''):
    """
    A context manager for timing sections of code.
    :type name: str
    :param name: The name you want to give the contextified code

    Example
    ---------------------------------------------------------------------------
    # this code in a python script
    import time
    from pandashells import Timer
    with Timer('entire script'):
        for nn in range(3):
            with Timer('loop {}'.format(nn + 1)):
                time.sleep(.1 * nn)

    # will generate the following on stdout
    [loop 1] Time: 0:00:00.000056
    [loop 2] Time: 0:00:00.100600
    [loop 3] Time: 0:00:00.200650
    [entire script] Time: 0:00:00.301556
    ---------------------------------------------------------------------------
    """
    tstart = datetime.datetime.now()
    stream = OutStream()
    yield
    if name:
        stream.write('[%s]\n' % name)
    stream.write('Time: %s\n' % (datetime.datetime.now() - tstart))
