import unittest
from validator import Validator

class TestValidatorMethods(unittest.TestCase):

	def setUp(self):
		self.validator = Validator(False)
		self.assertEqual(
			self.validator.valid, True,
			'Validator does not default to true'
		)

	def tearDown(self):
		del self.validator

	def errors(self, num):
		self.assertEqual(
			len(self.validator.errors), num,
			'does not properly aggregate errors'
		)

	def test_valid_validate_timestamp(self):
		self.validator.validate_timestamp(1551140352)
		self.assertEqual(
			self.validator.valid, True,
			'validate_timestamp: incorrectly parsed numeric timestamp'
		)

		self.validator.validate_timestamp('1551140352')
		self.assertEqual(
			self.validator.valid, True,
			'validate_timestamp: incorrectly parsed string timestamp'
		)

	def test_invalid_validate_timestamp(self):
		self.validator.validate_timestamp(None)
		self.assertEqual(
			self.validator.valid, False,
			'validate_timestamp: does not fail properly on None'
		)
		self.validator.validate_timestamp('')
		self.assertEqual(
			self.validator.valid, False,
			'validate_timestamp: does not fail properly empty string'
		)
		self.validator.validate_timestamp('abcde')
		self.assertEqual(
			self.validator.valid, False,
			'validate_timestamp: does not fail properly alphabetic string'
		)
		self.errors(3)


	def test_valid_validate_time(self):
		self.validator.validate_time(10)
		self.assertEqual(
			self.validator.valid, True,
			'validate_time: fails on number'
		)
		self.validator.validate_time('10')
		self.assertEqual(
			self.validator.valid, True,
			'validate_time: fails on string value of a number'
		)

	def test_invalid_validate_time(self):
		self.validator.validate_time(None)
		self.assertEqual(
			self.validator.valid, False,
			'validate_time: does not fail on none value'
		)
		self.validator.validate_time('abc')
		self.assertEqual(
			self.validator.valid, False,
			'validate_time: does not fail on alphabetic string'
		)
		self.validator.validate_time('')
		self.assertEqual(
			self.validator.valid, False,
			'validate_time: does not fail on empty string'
		)
		self.errors(3)

	def test_valid_validate_UUID(self):
		pattern = self.validator.createRegexPattern('[0-5]')
		self.validator.validate_UUID('36b2355d-1eda-4a02-82c9-e0ee1fcea334', pattern)
		self.assertEqual(
			self.validator.valid, True,
			'validate_UUID: fails on a valid UUID'
		)

	def test_invalid_validate_UUID(self):
		pattern = self.validator.createRegexPattern('[0-5]')
		self.validator.validate_UUID('36b2355d-1eda-9a02-82c9-e0ee1fcea334', pattern)
		self.assertEqual(
			self.validator.valid, False,
			'validate_UUID: does not fail on an invalid Version UUID'
		)
		self.validator.validate_UUID('36b2355d-1eda-9a02-82c9-e0ee1fcea', pattern)
		self.assertEqual(
			self.validator.valid, False,
			'validate_UUID: does not fail on a too short UUID string'
		)
		self.errors(2)

	def test_valid_validate_sha(self):
		self.validator.validate_sha('682bf8c6b34650fd70339679de1b0ea8b908aeb65b44cc829c7126444229dae6')
		self.assertEqual(
			self.validator.valid, True,
			'validate_sha: fails on a valid sha256 string'
		)

	def test_invalid_validate_sha(self):
		self.validator.validate_sha('682bf8c6b34650fd70339679de1b0ea8b908aeb65b44cc829c71264442e6')
		self.assertEqual(
			self.validator.valid, False,
			'validate_sha: does not fail on a sha string which is too short'
		)
		self.validator.validate_sha('682bf8c6b34650fd70339679de1b0ea8b908aeb65b44cc829c7126444243432344324e6')
		self.assertEqual(
			self.validator.valid, False,
			'validate_sha: does not fail on a sha string which is too long'
		)
		self.validator.validate_sha('682bf8c6b34650fd70339679de1b0ea8b908aeb6Hb44cc829c7126444229dae6')
		self.assertEqual(
			self.validator.valid, False,
			'validate_sha: does not fail on a sha string which contains non-hex characters'
		)
		self.errors(3)

	def test_valid_validate_filename(self):
		result = self.validator.validate_file_name('foo.ext')
		self.assertEqual(result.ext, '.ext', 'validate_filename: extension fails on a valid filename')
		self.assertEqual(result.name, 'foo', 'validate_filename: name fails on a valid filename')

	def test_invalid_validate_filename(self):
		result = self.validator.validate_file_name('foo')
		self.assertEqual(result, None, 'validate_filename: does not fail on a file with no extension')
		self.errors(1)

	def test_valid_validate_path(self):
		self.validator.validate_path('/test/path/foo.exe', 'foo.exe')
		self.assertEqual(
			self.validator.valid, True,
			'validate_path: fails when end of path matches filename'
		)
		self.validator.validate_path('foo.exe', 'foo.exe')
		self.assertEqual(
			self.validator.valid, True,
			'validate_path: fails when path and filename are the same'
		)

	def test_invalid_validate_path(self):
		self.validator.validate_path('/test/path/foo', 'foo.exe')
		self.assertEqual(
			self.validator.valid, False,
			'validate_path: does not fail if the path and filename are different'
		)
		self.errors(1)

	def test_valid_validate_disposition(self):
		self.validator.validate_disposition(1)
		self.validator.validate_disposition(2)
		self.validator.validate_disposition(3)
		self.assertEqual(
			self.validator.valid, True,
			'validate_disposition: fails on valid disposition values'
		)

	def test_invalid_validate_disposition(self):
		self.validator.validate_disposition('a')
		self.validator.validate_disposition('0.5')
		self.validator.validate_disposition('4')
		self.assertEqual(
			self.validator.valid, False,
			'validate_disposition: does not fail on invalid disposition values'
		)
		self.errors(3)

	def test_valid_file_parse(self):
		file_record = {
			'ts': 15432123,
			'pt': 30,
			'sha': '682bf8c6b34650fd70339679de1b0ea8b908aeb65b44cc829c7126444229dae6',
			'ph': '/foobar/foo.txt',
			'nm': 'foo.txt',
			'dp': 1,
			'si': '0b2414c7-6002-44bc-907d-9ff641992e73',
			'uu': '0b2414c7-6002-44bc-907d-9ff641992e74',
			'bg': '0b2414c7-6002-44bc-907d-9ff641992e75'
		}

		self.validator(file_record, 0)
		self.errors(0)
		self.assertEqual(
			self.validator.valid, True,
			'validate: fails on a valid file record'
		)

	def test_invalid_file_parse(self):
		file_record = {
			'ts': 'abcd',
			'pt': -1,
			'sha': '682bf8c4650fd70339679de1b0ea8b908aeb65b44cc829c7126444229dae6',
			'ph': '/foobar/foo.txt',
			'nm': 'foo',
			'dp': 5,
			'si': '0b2414c7-6002-64bc-907d-9ff641992e73',
			'uu': '0b2414c7-6002-74bc-907d-9ff641992e74',
			'bg': '0b2414c7-6002-84bc-907d-9ff641992e75'
		}

		self.validator(file_record, 0)
		self.errors(9)
		self.assertEqual(
			self.validator.valid, False,
			'validate: does not fail on an invalid file record'
		)

if __name__ == '__main__':
    unittest.main()