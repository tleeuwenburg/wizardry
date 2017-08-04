from wizardry.chunk import chunk

def test_chunk():

    c1 = chunk(12, 15, 14, 15)
    assert repr(c1) == 'From 12.00 to 15.00, the temperature will reach 15'


def test_multichunk():

    c1 = chunk(12, 15, 14, 15)
    c2 = chunk(15, 18, 12, 14)

    c = chunk(c1, c2)


# from wizardry import chunker
#
# def test_basic_chunk():
#
#     inputs = [
#         (0, 1, 11, 12),
#         (1, 2, 11, 11),
#         (2, 3, 11, 10),
#         (3, 4, 10, 10),
#         (4, 5, 10, 9),
#         (5, 6, 9, 9),
#     ]
#
#     c = chunker.chunk(inputs)
#     words = 'Hours 0 to 6, up to 12'
#
#     assert c.max == 12
#     assert repr(c) == words
#
# def test_multichunk():
#
#     inputs1 = [
#         (0, 1, 11, 12),
#         (1, 2, 11, 11),
#         (2, 3, 11, 10),
#     ]
#     c1 = chunker.chunk(inputs1)
#
#     inputs2 = [
#         (3, 4, 10, 10),
#         (4, 5, 10, 9),
#         (5, 6, 9, 9),
#     ]
#     c2 = chunker.chunk(inputs2)
#
#     c = chunker.chunk([c1, c2])
#     assert c.max == 12
#
#     words = 'Hours 0 to 2, up to 12\n'
#     words += 'Hours 3 to 5, up to 10'
#     assert repr(c) == words
