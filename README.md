# PyModMonTest
Python Modbus Monitor for test

Modification of PyModMon to add a new interface to follow the test of our PV-storage-system.
These tests follows instruction from the BVES: Effizienzleitfaden für PV-Speichersysteme (Version 2.0.1)
You can refind this file on: https://www.bves.de/technische-dokumente/

# PyModMon
Python Modbus Monitor

This is a Python skript that acts as a Modbus slave.
It can be used e.g. for reading data from newer solar inverters made by SMA.

It has the ability to monitor several modbus addresses with a configurable interval and can also write the received data to a csv file.

The logged data can then be used with other programs for analysing or plotting.

Dependencies:
* Python 2.7
* Python package docopt
* Python package pymodbus (and dependencies)

pymodmon_3.py is the updated version for Python 3 (tested with Python 3.7). No additional functionality was added.
