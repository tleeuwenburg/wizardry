def all_sublists(alist, depth):

    head = alist
    tail = []

    split = [head, tail]
    all_splits = [split]

    if depth > 0:

        for i in range(1, len(alist)):
            head, tail = [alist[:i], alist[i:]]
            rests = all_sublists(tail, depth -1)

            for rest in rests:
                rest = [r for r in rest if r]
                all_splits.append([head] + rest)

    return all_splits
