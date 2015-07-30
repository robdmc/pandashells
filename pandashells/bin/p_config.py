#! /usr/bin/env python

# --- standard library imports
import os
import sys  # noqa  Not used in code, but patched in testing
import argparse
import textwrap

from pandashells.lib import config_lib


def main():
    # --- read in the current configuration
    default_dict = config_lib.get_config()

    msg = textwrap.dedent(
        """
        Sets the default IO and plotting behavior for the pandashells toolset
        by creating/modifying a hidden configuration file (~/.pandashells)

        -----------------------------------------------------------------------
        Examples:

            * Show the current configuration
                p.config

            * Set the configuration to "factory defaults"
                p.config --force_defaults

            * Set default input/output to assume white-space delimited columns
              with no headers.
                p.config --io_input_header noheader --io_input_type table
                p.config --io_output_header noheader --io_output_type table
        -----------------------------------------------------------------------
        """
    )

    # --- populate the arg parser with current configuration
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)
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
    config_dict = {t[0]: t[1][0] for t in args.__dict__.items()
                   if not t[0] in ['force_defaults']}

    if args.force_defaults:
        cmd = 'rm {} 2>/dev/null'.format(config_lib.CONFIG_FILE_NAME)
        os.system(cmd)
        config_dict = config_lib.DEFAULT_DICT
    config_lib.set_config(config_dict)

    sys.stdout.write('\n Current Config\n')
    sys.stdout.write('  ' + '-' * 40 + '\n')
    for k in sorted(config_dict.keys()):
        if k not in ['--force_defaults']:
            sys.stdout.write(
                '  {: <20} {}\n'.format(k + ':', repr(str(config_dict[k]))))


if __name__ == '__main__':  # pragma: no cover
    main()
