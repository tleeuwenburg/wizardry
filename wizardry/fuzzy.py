from functools import reduce
import Levenshtein as lv
import math
import operator

ALPHA = 0.01  # To avoid zero vaues in multiply and divide


def learn(books):
    '''
    @return an agent that knows about all the books
    '''

    agent = Agent()

    for title, author, lines in books:
        agent.learn(title, author, lines)

    return agent

def score_words(word1, word2):
    '''
    @return a number between 0 and 1, where 0 = perfect match

    Uses a scaled version of the edit distance and the tanh function.
    '''

    distance = lv.distance(word1, word2)
    scaled = distance / 3
    score = math.tanh(scaled) + ALPHA
    return score

def best_match(xs, ys):
    '''
    Return the two strings which best match between xs and ys
    '''

    matches = []
    for x in xs:
        sorted_ys = sorted((score_words(x, y), y) for y in ys)
        y = sorted_ys[0][1]
        matches.append((x, y))

    best_match = matches[0]
    return best_match

def match(hasha, hashb):

    xs = [x.strip().lower() for x in hasha.split()]
    ys = [y.strip().lower() for y in hashb.split()]

    length = min(len(xs), len(ys))

    matches = []
    for i in range(length):
        x, y = best_match(xs, ys)
        xs.remove(x)
        ys.remove(y)
        matches.append((x, y))

    scores = [score_words(x, y) for (x, y) in matches]
    score = reduce(operator.mul, scores)

    return score



class Agent():

    def __init__(self):
        self.dict = {}
        self.authors = []
        self.titles = []
        self.mode = None

    def set_mode(self, mode):
        self.mode = mode

    def learn(self, title, author, lines):

        terrible_hash = title + " " + author
        self.dict[terrible_hash] = (title, author, lines)

    def __getitem__(self, search_term):

        items = list(self.dict.items())
        best_score = 50
        best_item = None

        for (key, value) in items:
            title, author, lines = value
            terrible_hash = title + "    " + author
            score = match(search_term, terrible_hash)

            if self.mode == 'show_scores':
                print("Matching %s and %s: %s" % (search_term, terrible_hash, score))

            if score < best_score:
                best_score = score
                best_item = value


        return best_item
