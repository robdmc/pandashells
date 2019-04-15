#! /usr/bin/env python

import argparse
import textwrap
import os
import sys


def main():
    msg = textwrap.dedent(
        """
        Encrypts and decrypts files using openssl.  Openssl provides command-
        line tools that are capable of encrypting and decrypting files.  This
        tool provides a thin wrapper around that capability by hardcoding
        the encyrption to be aes256-cbc.

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
        '-o', '--outFile', nargs=1, type=str, required=True, dest='outFile',
        metavar='outFileName', help="The output file name")

    parser.add_argument(
        '--password', nargs=1, type=str, dest='password',
        help="Avoid using this argument.  You will be prompted for password")

    msg = 'Decrypt the input file into the output file'
    parser.add_argument(
        '-d', '--decrypt', action='store_true', default=False, dest='decrypt',
        help=msg)

    msg = 'Echo encryption command to stdout'
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False, dest='verbose',
        help=msg)

    msg = 'Use legacy md5 digest'
    parser.add_argument(
        '-m', '--md5', action='store_true', default=False, dest='md5',
        help=msg)

    #  parse arguments
    args = parser.parse_args()

    #  make sure input file exists
    if not os.path.isfile(args.in_file[0]):
        sys.stderr.write(
            "\n\nCan't find input file: {}\n\n".format(args.in_file[0]))
        sys.exit(1)

    # populate a password string
    password_string = "-k '{}'".format(
        args.password[0]) if args.password else ''

    # set the proper decrypt digest string
    if args.md5:
        digest_str = '-md md5'
    else:
        digest_str = '-pbkdf2'

    # create a decryption command if requested
    if args.decrypt:
        cmd = "cat {} | openssl enc -d -aes-256-cbc {} {} > {}".format(
            args.in_file[0],
            password_string,
            digest_str,
            args.outFile[0]
        )
    #  otherwise just encrypt
    else:
        cmd = "cat {} | openssl enc -aes-256-cbc -pbkdf2 -salt {} > {}".format(
            args.in_file[0], password_string, args.outFile[0])

    # print verbose if requested
    if args.verbose:
        sys.stdout.write('\n\nExecuting:\n{}\n\n'.format(cmd))
    #  run the proper openssl command
    os.system(cmd)

if __name__ == '__main__':  # pragma: no cover
    main()
