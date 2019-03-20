# log-examine

A Python scipt which take in a file of JSON objects acting as file logs and reads them in one at a time.
Returns a printout of unique extensions and how many times they appear within the log.

Only valid file logs in all field are parsed and logged.

To run the file, run:

`python ./main.py <filename>`

This will print the output to the console in the form of:

```
.foo: <count>
.bar: <count>
```

If the file contains invalid entries and they should be printed to the console,
run the command

`python './main.py <filename> [-v, --verbose]`


To run the unit tests, run:

`python './validator.test.py`
