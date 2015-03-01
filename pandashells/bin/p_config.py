#! /usr/bin/env python

# --- standard library imports
import os
import sys  # noqa  Not used in code, but patched in testing
import argparse

from pandashells.lib import config_lib


def main():
    # --- read in the current configuration
    default_dict = config_lib.get_config()

    #TODO: write docs here
    msg = "Need to write this. "
    msg += "and write more."

    # --- populate the arg parser with current configuration
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument('--force_defaults', action='store_true',
                        dest='force_defaults',
                        help='Force to default settings')
    for tup in config_lib.CONFIG_OPTS:
        msg = 'opts: {}'.format(str(tup[1]))
        parser.add_argument('--%s' % tup[0], nargs=1, type=str,
                            dest=tup[0], metavar='',
                            default=[default_dict[tup[0]]],
                            choices=tup[1], help=msg)

    # --- parse arguments
    args = parser.parse_args()

    # --- set the arguments to the current value of the arg parser
    config_dict = {t[0]: t[1][0] for t in args.__dict__.iteritems()
                   if not t[0] in ['force_defaults']}

    if args.force_defaults:
        cmd = 'rm {} 2>/dev/null'.format(config_lib.CONFIG_FILE_NAME)
        os.system(cmd)
        config_dict = config_lib.DEFAULT_DICT
    config_lib.set_config(config_dict)

    print '\n Current Config'
    print '  ' + '-' * 40
    for k in sorted(config_dict.keys()):
        if k not in ['--force_defaults']:
            print '  {: <20} {}'.format(k + ':', repr(str(config_dict[k])))


if __name__ == '__main__':  # pragma: no cover
    main()
