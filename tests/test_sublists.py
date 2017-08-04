from wizardry.utils import all_sublists


def test_sublists():

    sample_list = [1,2,3,4,5]
    d0 = [
        [[1,2,3,4,5], []]
    ]

    found = all_sublists(sample_list, 0)
    assert found == d0

    depth_one = [
        [[1, 2, 3, 4, 5],[]],
        [[1], [2, 3, 4, 5]],
        [[1, 2], [3, 4, 5]],
        [[1, 2, 3], [4, 5]],
        [[1, 2, 3, 4], [5]]
    ]
    assert depth_one == all_sublists(sample_list, 1)

    depth_two = [
        [[1], [2], [3, 4, 5]],
        [[1], [2, 3], [4, 5]],
        [[1], [2, 3, 4], [5]],
        [[1, 2], [3], [4, 5]],
        [[1, 2], [3, 4], [5]],
        [[1, 2, 3], [4], [5]],
    ]

    d2 = all_sublists(sample_list, 2)
    for split in depth_one:
        assert split in d2

    for split in depth_two:
        assert split in d2
