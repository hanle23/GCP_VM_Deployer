#!/usr/bin/python3
import os
import sys
import subprocess
from pathlib import Path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def open_file(name):
    try:
        file = open(os.path.join(__location__, name), "a")
    except FileNotFoundError:
        return False
    else:
        return file


def create_file(name):
    file = open(os.path.join(__location__, name), "x")
    return file


def remake_file(name):
    file = open(os.path.join(__location__, name), "w")
    return file


def runcommand(command):
    subprocess.run(command)


def run(name):
    return Path('test.py').open()


fileName = input(": ")
print(run(fileName))
