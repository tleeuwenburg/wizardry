from plotly.graph_objs import Scatter, Bar, Figure, Layout
import operator

from functools import reduce
from wizardry.utils import all_sublists

def chunk(*values):
    '''
    Take pretty broad-ranging input, and chunk it. Chunky.
    '''

    try:

        if isinstance(values[0], Chunk):
            return MultiChunk(values)

        if isinstance(values[0], list):
            parts = [TinyChunk(v) for v in values[0]]
            chunk = MultiChunk(parts)
            return chunk

        return TinyChunk(values)

    except:
        print(values)
        raise


class Chunk():

    def __repr__(self):

        return self.basic_words()


    def error(self):
        raise NotImplementedError

    def basic_words(self):
        tpl = "From %2.2f to %2.2f, the temperature will reach %s"
        tpl = tpl % (self.start, self.end, self.max)

        return tpl

    def __add__(self, other):

        if isinstance(other, str):
            return repr(self) + other

        return MultiChunk([self, other], mode='aggregate')

    def __radd__(self, other):

        return other + repr(self)

    def set_previous(self, prev):
        self.prev = prev

    def fig(self):

        durations = self.durations()

        if max(durations) > 2:
            return self.figure_bar()

        return self.figure_scatter()

    def figure_bar(self):

        starts = self.starts()
        ends = self.ends()

        xs = list(round((start + end)/2) for start, end in zip(starts, ends))
        ys = list(self.maxs())
        durations = list(self.durations())

        b_trace = Bar(x=xs,
                      y=ys,
                      width=durations)

        layout = Layout(
            xaxis=dict(range=[0, 24]),
            yaxis=dict(range=[5, 18])
        )

        fig = Figure(data=[b_trace], layout=layout)
        return fig

        #
        # trace0 = Bar(
        #     x=[1, 2, 3, 5.5, 10],
        #     y=[10, 8, 6, 4, 2],
        #     width = [0.8, 0.8, 0.8, 3.5, 4]
        # )
        #
        # data = [trace0]
        #
        # fig = Figure(data=data)
        # iplot(fig)

    def figure_scatter(self):

        starts = list(self.starts())
        maxs = list(self.maxs())
        durations = list(self.durations())

        trace = Scatter(x=starts,
                    y=maxs,)
        layout = Layout(
            xaxis=dict(range=[0, 24]),
            yaxis=dict(range=[5, 18])
        )
        fig = Figure(data=[trace], layout=layout)
        return fig

class MultiChunk(Chunk):

    def __init__(self, values, mode='sequence'):

        if len(values) == 0:
            raise Exception("Cannot create an empty multichunk")

        # Multichunk components must be other chunks
        for v in values:
            assert isinstance(v, Chunk)

        self.subchunks = values
        self.set_previous(None)
        self.mode = mode

        for i in range(1, len(values)):
            values[i].set_previous(values[i-1])


    def error_sequence(self):
        '''
        1 is a perfect score
        0 is the worst score
        '''

        errors = [c.error() for c in self.subchunks]
        error = reduce(operator.add, errors)

        return error

    def error_aggregate(self):

        overall_max = self.max

        maxs = [c.max for c in self.subchunks]
        errors = [(overall_max - m) / overall_max for m in maxs]
        cum_error = reduce(operator.add, errors)

        return cum_error


    def error(self):
        '''
        The score of a sequence is a funtion of the scores of its
        components.

        The score of an aggregate is a function of the relationship between
        its components and its summary.

        1 is a perfect score
        0 is the worst score
        '''


        if self.mode == "aggregate":
            return self.error_aggregate()

        else:
            return self.error_sequence()

    def __repr__(self):

        if self.mode == 'sequence':
            return self.sequence_words()

        if self.mode == 'aggregate':
            return self.basic_words()

    def sequence_words(self):

        parts = []
        tpl = ''
        for c in self.subchunks:
            parts.append(repr(c))

        tpl += ' and '.join(parts)
        return tpl

    def dumbchunk(self):

        chunk_len = 6
        parts = []
        for i in range(0, len(self.subchunks), chunk_len):
            bigchunk = MultiChunk(self.subchunks[i:i+chunk_len], mode='aggregate')
            parts.append(bigchunk)

        self.subchunks = parts

    def smartchunk(self):

        chunk_max_count = 3

        foo = []

        all_splits = all_sublists(self.subchunks, depth=chunk_max_count)

        for splits in all_splits:
            parts = []
            for split in splits:
                if len(split) > 0:
                    bigchunk = MultiChunk(split, mode='aggregate')
                    parts.append(bigchunk)

            seq = MultiChunk(parts, mode='sequence')
            foo.append(seq)

        scores = [(f.error(), f) for f in foo if f.error() != 0]

        errors, fs = zip(*scores)

        scores.sort(key=operator.itemgetter(0))
        best_score, best_combo = scores[0]
        self.subchunks = best_combo.subchunks


    @property
    def start(self):
        starts = [c.start for c in self.subchunks]
        return min(starts)

    @property
    def end(self):
        ends = [c.end for c in self.subchunks]
        return max(ends)

    @property
    def max(self):

        try:
            maxs = [c.max for c in self.subchunks]
            overall_max = max(maxs)

        except:

            print(self.mode)
            print(len(self.subchunks))
            raise

        return overall_max

    @property
    def min(self):
        mins = [c.min for c in self.subchunks]
        return min(mins)

    def starts(self):
        return [c.start for c in self.subchunks]

    def ends(self):
        return [c.end for c in self.subchunks]

    def maxs(self):
        return [c.max for c in self.subchunks]

    def mins(self):
        return [c.min for c in self.subchunks]

    def durations(self):
        return list([a - b for (a, b) in zip(self.ends(), self.starts())])

class TinyChunk(Chunk):

    def __init__(self, values):

        start, end, amin, amax = values
        self.start = start
        self.end = end
        self.max = amax
        self.min = amin

        self.set_previous(None)

    def error(self):
        '''
        0 is a perfect score
        1 is the worst score
        '''

        return 0  # TinyChunks perfectly represent the data
















#
#     def smartchunk(self):
#         depth = 2
#         options = all_sublists(self.chunks, depth)
#         scores = self.score(options)
#         sort(scores)
#
#         score, chunks = scores[0]
#         self.chunked = chunks
#
#
#
#     def scores(self, options):
#
#         scores = []
#         for option in options:
#             score = self.score_max(option)
#             scores.append(score, option)
#
#         return scores
#
#
