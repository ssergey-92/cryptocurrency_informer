"""Module to init package and add package path to system paths for pytest."""
from os import path as os_path
from sys import path as sys_path

sys_path.append(os_path.dirname(os_path.realpath(__file__)))