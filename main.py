#! /usr/bin/env python
"""
A skeleton python script which reads from an input file,
writes to an output file and parses command line arguments
"""
import sys
import argparse
import json

def get_cli_input():
		parser = argparse.ArgumentParser(description=__doc__)
		parser.add_argument('input', help='path to the input file', metavar='INPUT_FILE')
		args = parser.parse_args()

		return args

def main():

	args = get_cli_input()
	# TODO: Validate the input
	with open(args.input, 'r') as file:
		# TODO: cast into a list
	

	# TODO: For Loop
		# TODO: Cast to json and cath error
		# TODO: Validate timestamps
		# TODO: validate UUID4'
		# TODO: validate the sha256
		# TODO: validate the disposition
		# TODO: validate the name has a filename.extension format
		# TODO: validate the path is a correct relative path
		# TODO: Create a dict of sets. Key is the extension, value is the set of names
	# TODO: End loop
	# TODO: count the set sizes and return the key:size dict


	#my_list = [json.loads(line.rstrip('\n')) for line in args.input]

	#print(my_list[0].keys())
	# for line in args.input:

	#     print(line.strip(), file=args.output)




























if __name__ == "__main__":
		main()