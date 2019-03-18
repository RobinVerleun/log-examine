#! /usr/bin/env python
'''
	A program which takes in an input file of json log entries and counts the number
	of unique occurances of each extension type.

	By: Robin Verleun
'''
import sys
import argparse
import json

from operator import itemgetter
import datetime
import re

def get_cli_input():
		parser = argparse.ArgumentParser(description=__doc__)
		parser.add_argument('input', help='path to the input file', metavar='INPUT_FILE')
		args = parser.parse_args()

		return args

# Source: https://gist.github.com/kgriffs/c20084db6686fee2b363fdc1a8998792
def createRegexPattern(version):
	return re.compile(
		(
			'[a-f0-9]{8}-' +
			'[a-f0-9]{4}-' +
			version + '[a-f0-9]{3}-' +
			'[89ab][a-f0-9]{3}-' +
			'[a-f0-9]{12}$'
		),
		re.IGNORECASE
	)

def validate_file_log(file, index):
	# print('{0}    :{1}'.format(index, file))

	# Valid flag for tracking the progress of the file validation
	valid = True;
	
	validate_timestamp(file['ts'])
	validate_time(file['pt'])

	all_pattern = createRegexPattern('[0-5]')
	validate_UUID(file['si'], all_pattern)
	validate_UUID(file['uu'], all_pattern)
	validate_UUID(file['bg'], all_pattern)

	# validate_file_name(file['nm'])
	# validate_path(file['ph'])
	
	# validate_disposition(file['dp'])

'''
	Take in a Unix millisecond timestamp and verify it by casting it to
	a new datetime object. 
'''
def validate_timestamp(time):
	try:
		timestamp = datetime.datetime.fromtimestamp(time)
		return True
	except:
		print('Invalid timestamp')
		return False

'''
	Take in a time value and verify that it is a positive number or 0
'''
def validate_time(time):
	try:
		return (True if int(time) >= 0 else False)
	except:
		print('Invalid time value')
		return False

'''
	Take in a UUID string and attempt to verify it as a 8-4-4-4-12 format
	string using regex. Does not enforce a version value, as specified in 
	the response to the email.

	Otherwise, we could just test for UUIDv4 using the UUID package and casting
	the string to a new UUID.
'''
def validate_UUID(uuid_to_test, pattern):

	if(len(uuid_to_test) != 36): 
		print('Invalid UUID Length:', uuid_to_test)
		return False
	
	if(pattern.match(uuid_to_test)):
		return True
	else:
		print('Invalid UUID:', uuid_to_test)
		return False 

def validate_file_name(name):
	return


def validate_path(path):
	return


def validate_disposition(dp):
	return



def main():
	args = get_cli_input()

	# try:except block to catch file open errors.
	try:
		with open(args.input, 'r') as file:
			for num, line in enumerate(file, start=1):

				try:
					json_file = json.loads(line)
					validate_file_log(json.loads(line), num)
				except:
					print('Issue loading line {}'.format(num))
					
	except Exception as e:
		print('Error: {}', e)



# Execute main function
if __name__ == "__main__":
	main()


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