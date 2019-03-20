#! /usr/bin/env python
'''
    A program which takes in an input file of json log entries and counts the number
    of unique occurances of each extension type.

    By: Robin Verleun
'''
import sys
import argparse
import json
import re
from collections import defaultdict

from validator import Validator

def get_cli_input():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='path to the input file', metavar='INPUT_FILE')
    parser.add_argument('-v', '--verbose',
                        dest='verbose', help='output line errors', action='store_true')
    args = parser.parse_args()

    return args

def print_result(extensions):
    '''
        Takes in a dictionary and print the key with the size of the corresponding set.
    '''
    for key, value in extensions.items():
        print('{0}: {1}'.format(key, len(value)))


def main():

    args = get_cli_input()

    # try:except block to catch file open errors.
    try:
        with open(args.input, 'r') as file:

            extension_set = defaultdict(set)
            line_validator = Validator(args.verbose)

            # loop over the values, attempting to validate.
            for linenum, line in enumerate(file, start=1):
                try:
                    json_file = json.loads(line)
                    result = line_validator(json.loads(line), linenum)

                    if result is None:
                        continue

                    extension_set[result.ext].add(result.name)

                except Exception as e:
                    print('Issue loading line {0}: {1}'.format(linenum, e))

            print_result(extension_set)

    except Exception as e:
        print('Error', e)



# Execute main function
if __name__ == "__main__":
    main()
