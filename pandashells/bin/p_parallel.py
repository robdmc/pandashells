#! /usr/bin/env python

import sys
import argparse
import textwrap

from pandashells.lib import parallel_lib


def main():
    msg = "Tool to run shell commands in parallel.  Spawns processes "
    msg += "to concurrently run commands supplied on stdin. "

    msg = textwrap.dedent(
        """
        Read a list of commands from stdin and execute them in parrallel.

        -----------------------------------------------------------------------
        Examples:

            * This line generates commands that will be used in the examples.
                time seq 10 \\
                | p.format -t 'sleep 1; echo done {n}' --names n -i noheader

            * Execute the commands one at a time, no parallelism
                time seq 10 \\
                | p.format -t 'sleep 1; echo done {n}' --names n -i noheader \\
                | p.parallel -n 1

            * Execute all commands in parallel
                time seq 10 \\
                | p.format -t 'sleep 1; echo done {n}' --names n -i noheader \\
                | p.parallel -n 10

            * Suppress stdout from processes and echo commands
                time seq 10 \\
                | p.format -t 'sleep 1; echo done {n}' --names n -i noheader \\
                | p.parallel -n 10 -c -s stdout

            * Make a histogram of how long the individual jobs took
                time seq 100 \\
                | p.format -t 'sleep 1; echo done {n}' --names n -i noheader \\
                | p.parallel -n 50 -v \\
                | grep __job__ \\
                | p.df 'df.dropna()' 'df.duration_sec.hist(bins=20)'
        -----------------------------------------------------------------------
        """
    )

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    msg = "The number of jobs to run in parallel. If not supplied, will "
    msg += "default to the number of detected cores."
    parser.add_argument('--njobs', '-n', dest='njobs', default=[None],
                        nargs=1, type=int, help=msg)
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Enable verbose output")

    parser.add_argument("-c", "--show_commands", action="store_true",
                        default=False, help="Print commands to stdout")

    msg = "Suppress stdout, stderr, or both for all running jobs"
    parser.add_argument("-s", "--suppress",
                        choices=['stdout', 'stderr', 'both'], default=[None],
                        nargs=1, help=msg)

    # parse arguments
    args = parser.parse_args()

    # get the commands from stdin
    cmd_list = sys.stdin.readlines()

    # get suppression vars from args
    suppress_stdout = 'stdout' in args.suppress or 'both' in args.suppress
    suppress_stderr = 'stderr' in args.suppress or 'both' in args.suppress

    # run the commands
    parallel_lib.parallel(
        cmd_list,
        njobs=args.njobs[0],
        verbose=args.verbose,
        suppress_cmd=(not args.show_commands),
        suppress_stdout=suppress_stdout,
        suppress_stderr=suppress_stderr,
        assume_hyperthread=True)

if __name__ == '__main__':  # pragma: no cover
    main()
