import builtins
import random

from unittest.mock import patch

real_print = builtins.print

def print_and_fuzz(*args):
    new_args = [a + random.random() for a in args]
    real_print(*new_args)

def mystify():
    o = patch('builtins.print', new=print_and_fuzz)
    return o
