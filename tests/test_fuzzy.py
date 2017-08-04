import wizardry.fuzzy as fz

def test_best_match():
  xs = "hello world".split()
  ys = "hello goodbye".split()

  expected = ("hello", "hello")
  found = fz.best_match(xs, ys)

  assert found == expected

def test_match():

    first = "Hello how are you"
    second = "Hello is not the only word"

    score_perfect = fz.match(first, first)
    score_worse = fz.match(first, second)

    assert score_perfect < score_worse
