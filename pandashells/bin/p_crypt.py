#! /usr/bin/env python

import argparse
import os
import re
import sys

from pandashells.lib import arg_lib

def main():
    msg = "Encrypt a file with aes-256-cbc as implemented by openssl. "

    #  read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'example')

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

    #  create a dycryption command if requested
    if args.decrypt:
        cmd = "cat {} | openssl enc -d -aes-256-cbc {} > {}".format(
            args.in_file[0], password_string, args.outFile[0])
    #  otherwise just encrypt
    else:
        cmd = "cat {} | openssl enc -aes-256-cbc -salt {} > {}".format(
            args.in_file[0], password_string, args.outFile[0])

    # print verbose if requested
    if args.verbose:
        sys.stdout.write('\n\nExecuting:\n{}\n\n'.format(cmd))
    #  run the proper openssl command
    os.system(cmd)

if __name__ == '__main__': # pragma: no cover

    main()
