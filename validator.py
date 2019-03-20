
import os
import re
from datetime import datetime
from collections import namedtuple
Result = namedtuple('result', ['name', 'ext'])

MALICIOUS = 1
CLEAN = 2
UNKNOWN = 3

class Validator:
    '''
        Class which holds the state and process for validating a json file log.
        takes in
    '''
    def __init__(self, verbose):
        self.valid = True
        self.errors = []
        self.verbose = verbose

    def __del__(self):
        return

    def validate_timestamp(self, time):
        '''
            time: Unix timestamp. Can be a number or string
            Take in a Unix millisecond timestamp and verify it by casting it to
            a new datetime object.
        '''
        try:
            num_time = int(time)
            datetime.fromtimestamp(num_time)
        except:
            self.valid = False
            self.errors.append('Invalid timestamp ({0})'.format(time))


    def validate_time(self, time):
        '''
            time: Positive number
            Take in a time value and verify that it is a positive number or 0
        '''
        try:
            if int(time) < 0:
                raise ValueError('Invalid time')
        except:
            self.valid = False
            self.errors.append('Invalid time value ({0})'.format(time))


    def create_regex_pattern(self, version):
        # Source: https://gist.github.com/kgriffs/c20084db6686fee2b363fdc1a8998792
        return re.compile(
            (
                '[a-f0-9]{8}-' +
                '[a-f0-9]{4}-' +
                version + '[a-f0-9]{3}-' +
                '[89ab][a-f0-9]{3}-' +
                '[a-f0-9]{12}$'
            ), re.IGNORECASE
        )


    def validate_uuid(self, uuid_to_test, pattern):
        '''
            uuid_to_test: string representing a 8-4-4-4-12 uuid.
            pattern: compiled regex pattern

            Take in a UUID string and verify it as a 8-4-4-4-12 format
            string using regex. Does not enforce a version value, according to the
            clarification email.

            Otherwise, we could just test for UUIDv4 using the UUID package and casting
            the string to a new UUID.
        '''
        if len(uuid_to_test) != 36:
            self.valid = False
            self.errors.append('Invalid UUID length ({0})'.format(uuid_to_test))
            return
        if not pattern.match(uuid_to_test):
            self.valid = False
            self.errors.append('Invalid UUID format ({0})'.format(uuid_to_test))


    def validate_sha(self, sha):
        '''
            sha: string representing a sha256 value

            Take in a sha256 string and check to ensure it is:
                64 characters long
                Has only hexadecimal values
            The cast to int will error if invalid hex values are passed.
        '''
        if len(sha) != 64:
            self.valid = False
            self.errors.append('Invalid length for sha256 ({0})'.format(sha))
            return
        try:
            int(sha, 16)
        except:
            self.valid = False
            self.errors.append('Invalid sha256 value ({0})'.format(sha))


    def validate_file_name(self, name):
        '''
            name: filename to validate

            Confirm that the filename has an extension using the OS libraries.
        '''
        # Extract the name and extension from the filename and confirm the extension exists
        name, ext = os.path.splitext(name)
        if len(ext) == 0:
            self.valid = False
            self.errors.append('Filename has no extension ({0})'.format(name))
            return None
        return Result(name, ext)


    def validate_path(self, path, name):
        '''
            path: filepath to validate
            name: filename to compare against

            Take in a filepath and confirm that it matches the given filename in the log.
            Assumption: filepaths don't need leading or trailing slashes to be valid
            Assumption: filepath only needs the name of the file at the end to be valid
        '''
        _path, _file = os.path.split(path)
        if _file != name:
            self.valid = False
            self.errors.append('Path \'{0}\' does not match the given filename \'{1}\''.format(path, name))


    def validate_disposition(self, dp):
        '''
            dp: integer representing the files disposition.

            Check the disposition of the log. If it is not a value of 1, 2, or 3, it is considered invalid.
        '''
        try:
            disposition = int(dp)
            if not (disposition in [MALICIOUS, CLEAN, UNKNOWN]):
                raise ValueError
        except:
            self.valid = False
            self.errors.append('Dispositon is invalid ({0})'.format(dp))


    def reset_state(self):
        self.valid = True
        self.errors = []


    def print_errors(self, index):
        print('File number {0}:'.format(index))
        for error in self.errors:
            print('\t {0}'.format(error))


    def __call__(self, log, linenum):
        # Set the valid flag to true at the beginning of the validation pass
        # Clear the errors buffer
        self.reset_state()

        self.validate_timestamp(log['ts'])
        self.validate_time(log['pt'])
        self.validate_sha(log['sha'])
        self.validate_path(log['ph'], log['nm'])
        self.validate_disposition(log['dp'])

        all_pattern = self.create_regex_pattern('[0-5]')
        self.validate_uuid(log['si'], all_pattern)
        self.validate_uuid(log['uu'], all_pattern)
        self.validate_uuid(log['bg'], all_pattern)

        filename = self.validate_file_name(log['nm'])

        if self.valid:
            return filename
        else:
            if self.verbose:
                self.print_errors(linenum)
            return None
