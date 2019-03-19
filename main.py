#! /usr/bin/env python
'''
	A program which takes in an input file of json log entries and counts the number
	of unique occurances of each extension type.

	By: Robin Verleun
'''
import sys
import argparse
import json
import os
import datetime
import re
from collections import defaultdict


def get_cli_input():
		parser = argparse.ArgumentParser(description=__doc__)
		parser.add_argument('input', help='path to the input file', metavar='INPUT_FILE')
		parser.add_argument('--v', '--verbose', dest='verbose', help='output line errors', action='store_true')
		args = parser.parse_args()

		return args


'''
	Validate the fields of the file sequentially.
	Store the return from the name validation to re-use the name and extension
	for creating the dictionary entry at the end of the function.
'''
def validate_file_log(file, index):
	validate_timestamp(file['ts'])
	validate_time(file['pt'])
	validate_sha(file['sha'])
	validate_path(file['ph'], file['nm'])
	validate_disposition(file['dp'])

	all_pattern = createRegexPattern('[0-5]')
	validate_UUID(file['si'], all_pattern)
	validate_UUID(file['uu'], all_pattern)
	validate_UUID(file['bg'], all_pattern)
	
	name, ext = validate_file_name(file['nm'])

	return (name, ext)



'''
	Take in a Unix millisecond timestamp and verify it by casting it to
	a new datetime object. 
'''
def validate_timestamp(time):
	try:
		timestamp = datetime.datetime.fromtimestamp(time)
		return True
	except:
		raise ValueError('Value {0}: Invalid timestamp'.format(time))



'''
	Take in a time value and verify that it is a positive number or 0
'''
def validate_time(time):
	try:
		return (True if int(time) >= 0 else False)
	except:
		raise ValueError('Value {0}: Invalid time value'.format(time))



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



'''
	Take in a UUID string and verify it as a 8-4-4-4-12 format
	string using regex. Does not enforce a version value, according to the
	clarification email.

	Otherwise, we could just test for UUIDv4 using the UUID package and casting
	the string to a new UUID.
'''
def validate_UUID(uuid_to_test, pattern):

	if(len(uuid_to_test) != 36): 
		raise ValueError('Invalid UUID length')

	if(not pattern.match(uuid_to_test)):
		raise ValueError('Value {0}: Invalid UUID format'.format(uuid_to_test))



'''
	Take in a sha256 string and check to ensure it is:
		64 characters long
		Has only hexadecimal values
	The cast to int will error if invalid hex values are passed.
'''
def validate_sha(sha):
	if(len(sha) != 64):
		raise ValueError('Value {0}: Invalid length for sha256'.format(sha))
	try:
		int(sha, 16)
	except:
		raise ValueError('Value {0}: Invalid sha16 value'.format(sha))


'''
	Take in a filename and check to see if it starts or ends with slashes,
	then confirm it has an extension using the OS libraries.
'''
def validate_file_name(name):
	# Check that the filename doesn't start or end with a slash
	if(name.startswith(('/', '\\')) or name.endswith(('/', '\\'))):
		raise ValueError('Value {0}: Filename contains invalid slash characters.'.format(name))

	# Extract the name and extension from the filename and confirm the extension exists	
	name, ext = os.path.splitext(name)
	if(len(ext) == 0):
		raise ValueError('Value {0}: Filename has no extension'.format(name))
	return (name, ext)



'''
	Take in a filepath and confirm that it matches the given filename in the log.
	Assumption: filepaths don't need leading or trailing slashes to be valid
	Assumption: filepath only needs the name of the file at the end to be valid
'''
def validate_path(path, name):
	_path, _file = os.path.split(path)
	if(_file != name):
		raise ValueError('Path \'{0}\' does not match the given filename \'{1}\''.format(path, name))




'''
	Check the disposition of the log. If it is not a value of 1, 2, or 3, it is considered invalid.
'''
def validate_disposition(dp):
	try:
		disposition = int(dp)
		if(dp != 1 and dp != 2 and dp != 3):
			raise Exception
	except:
		raise ValueError('Value {0}: Dispositon is invalid'.format(dp))



def print_result(extensions):
	for key, value in extensions.items():
		print('{0}: {1}'.format(key, len(value)))


def main():
	args = get_cli_input()

	# try:except block to catch file open errors.
	try:
		with open(args.input, 'r') as file:

			extension_set = defaultdict(set);
			for num, line in enumerate(file, start=1):
			
				# loop over the values, attempting to validate. Catch ValueErrors thrown by the validator. 
				try:
					json_file = json.loads(line)
					name, ext = validate_file_log(json.loads(line), num)
					
					# If we're done validating without ValueError's, add to dict.
					extension_set[ext].add(name)
				
				except ValueError as value_error:
					if(args.verbose):
						print('Invalid line (#{0}): {1}'.format(num, value_error))
				except Exception as e:
					print('Issue loading line {0}: {1}'.format(num, e))

			print_result(extension_set)	

	except Exception as e:
		print('Error', e)



# Execute main function
if __name__ == "__main__":
	main()
