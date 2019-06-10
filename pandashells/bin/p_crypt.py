#! /usr/bin/env python

import argparse
import getpass
import textwrap
import os
import sys

from pandashells import Crypt


def main():
    msg = textwrap.dedent(
        """
        Encrypts and ecrypts files using the cryptography library for Python.

        See:
            https://cryptography.io/en/latest/fernet

        -----------------------------------------------------------------------
        Examples:

            * Encrypt an input file echoing the openssl command
                echo 'plain text' > file.txt
                p.crypt -i file.txt -v -o file.txt.crypt

            * Decrypt an input file
                p.crypt  -d -i file.txt.crypt -o file_restored.txt
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    parser.add_argument(
        '-i', '--in_file', nargs=1, type=str,
        required=True, dest='in_file', metavar='in_file_name',
        help="The input file name")

    parser.add_argument(
        '-o', '--out_file', nargs=1, type=str, required=True, dest='out_file',
        metavar='out_file_name', help="The output file name")

    parser.add_argument(
        '--password', nargs=1, type=str, dest='password',
        help="Avoid using this argument.  You will be prompted for password")

    msg = 'Decrypt the input file into the output file'
    parser.add_argument(
        '-d', '--decrypt', action='store_true', default=False, dest='decrypt',
        help=msg)

    msg = 'Save encrypted file to hex instead of binary'
    parser.add_argument(
        '--binary', action='store_true', default=False, dest='binary',
        help=msg)

    #  parse arguments
    args = parser.parse_args()

    #  make sure input file exists
    if not os.path.isfile(args.in_file[0]):
        sys.stderr.write(
            "\n\nCan't find input file: {}\n\n".format(args.in_file[0]))
        sys.exit(1)

    if args.password is None:
        password = getpass.getpass('Password: ')
    else:
        password = args.password[0]

    with open(args.in_file[0], 'rb') as f:
        in_value = f.read()

    if args.decrypt:
        out_value = Crypt().decrypt(in_value, password)
    else:
        out_value = Crypt().encrypt(in_value, password)

    with open(args.out_file[0], 'wb') as f:
        f.write(out_value)


"""
TODO: I want to add the options of piping from stdin and to stdout
Maybe make that the only option with no input and output files
"""


if __name__ == '__main__':  # pragma: no cover
    main()
