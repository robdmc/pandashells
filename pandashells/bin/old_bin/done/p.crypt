#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import arg_lib

# =============================================================================
if __name__ == '__main__':
    msg = "Encrypt a file with aes-256-cbc as implemented by openssl. "

    # --- read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.addArgs(parser, 'example')

    parser.add_argument('-i', '--inFile', nargs=1, type=str,
                        required=True, dest='inFile', metavar='inFileName',
                        help="The input file name")

    parser.add_argument('-o', '--outFile', nargs=1, type=str,
                        required=True, dest='outFile', metavar='outFileName',
                        help="The output file name")

    msg = 'Decrypt the input file into the output file'
    parser.add_argument('-d', '--decrypt', action='store_true', default=False,
                        dest='decrypt', help=msg)

    # --- parse arguments
    args = parser.parse_args()

    # --- make sure input file exists
    if not os.path.isfile(args.inFile[0]):
        sys.stderr.write("\n\nCan't find input file\n\n")
        sys.exit(1)

    # --- create a dycryption command if requested
    if args.decrypt:
        cmd = "cat %s | openssl enc -d -aes-256-cbc > %s" % (args.inFile[0],
                                                             args.outFile[0])
    # --- otherwise just encrypt
    else:
        cmd = "cat %s | openssl enc -aes-256-cbc -salt > %s" % (
            args.inFile[0], args.outFile[0])
    # --- run the proper openssl command
    os.system(cmd)
