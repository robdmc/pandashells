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


class TimerResult(object):
    def __init__(self, label, starting, ending=None, seconds=None):
        self.label = label
        self.starting = starting
        self.ending = ending
        self.seconds = seconds

    def __str__(self):
        return '__time__,{},{}'.format(self.seconds, self.label)

    def __repr__(self):
        return self.__str__()


@contextlib.contextmanager
def Timer(name='', silent=False, pretty=False):
    """
    A context manager for timing sections of code.
    :type name: str
    :param name: The name you want to give the contextified code
    :type silent: bool
    :param silent: Setting this to true will mute all printing
    :type pretty: bool
    :param pretty: When set to true, prints elapsed time in hh:mm:ss.mmmmmm
    Example
    ---------------------------------------------------------------------------
    # Example code for timing different parts of your code
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
    # Example for measuring how a piece of of code scales (measuring "big-O")
    import time
    from pandashells import Timer

    # initialize a list to hold results
    results = []

    # run a piece of code with different values of the var you want to scale
    for nn in range(3):
        # time each iteration
        with Timer('loop {}'.format(nn + 1), silent=True) as timer:
            time.sleep(.1 * nn)
        # add results
        results.append((nn, timer))

    # print csv compatible text for further pandashells processing/plotting
    print 'nn,seconds'
    for nn, timer in results:
        print '{},{}'.format(nn,timer.seconds)
    """
    stream = OutStream()
    result = TimerResult(name, starting=datetime.datetime.now())
    yield result
    result.ending = datetime.datetime.now()
    dt = result.ending - result.starting
    result.seconds = dt.total_seconds()
    dt = dt if pretty else result.seconds
    if not silent:
        stream.write('__time__,{},'.format(dt))
        if name:
            stream.write('%s\n' % name)
