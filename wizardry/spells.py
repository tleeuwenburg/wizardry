import builtins
import random

from unittest.mock import patch

real_print = builtins.print


class PlayingCard():

    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
        self.mode = 'bridge'

        self.bridge_suit_order = ['NT', "S", "H", "D", "C"]
        self.five_suit_order = ['NT', "H", "D", "C", "S"]
        self.suit_order = self.bridge_suit_order

    def __repr__(self):
        return "%s %s" % (self.value, self.suit)

    def set_mode(self, mode):

        if mode == 'bridge':
            self.suit_order = self.bridge_suit_order

        if mode == "500":
            self.suit_order = self.five_suit_order

        if mode == "random":
            random.shuffle(self.suit_order)

    def __gt__(self, other):

        if self.value > other.value:
            return True

        if self.value == other.value:
            if (self.suit_order.index(self.suit) <
                self.suit_order.index(other.suit)):
                return True

        return False

    def __lt__(self, other):
        return other > self

    def __eq__(self, other):

        if not self.suit == other.suit:
            return False

        if not self.value == other.value:
            return False

        return True


class OneIndexList(list):

    def __init__(self, content):
        self.content = list(content)

    def __getitem__(self, index):
        index -= 1
        return self.content[index]

class OneIndexCtx():

    def __init__(self, object):
        self.object = object


    def __enter__(self):

        self.original = self.object.copy()
        self.object['a'] = OneIndexList(self.object['a'])

    def __exit__(self, *args):
        self.object['a'] = self.original['a']



def print_and_fuzz(*args):
    new_args = [a + random.random() for a in args]
    real_print(*new_args)

def print_and_image(*args):

    new_args = [a + random.random() for a in args]
    real_print(*new_args)

    from PIL import Image
    im = Image.open("cat_plane.jpg")
    im.show()

def mystify():
    o = patch('builtins.print', new=print_and_fuzz)
    return o

def bamboozle():
    o = patch('builtins.print', new=print_and_image)
    return o


def index(a):

    OIC = OneIndexCtx(a)
    return OIC
