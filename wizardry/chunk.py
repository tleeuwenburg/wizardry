from plotly.graph_objs import Scatter, Bar, Figure, Layout
import operator

from wizardry.utils import all_sublists

def chunk(*values):


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


    def basic_words(self):
        tpl = "From %2.2f to %2.2f, the temperature will reach %s"
        tpl = tpl % (self.start, self.end, self.max)

        return tpl

    def __add__(self, other):

        if isinstance(other, str):
            return repr(self) + other

        return MultiChunk([self, other], mode='aggregate')

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

    def __init__(self, values, mode='seq'):

        # Multichunk components must be other chunks
        for v in values:
            assert isinstance(v, Chunk)

        self.subchunks = values
        self.set_previous(None)
        self.mode = mode

        for i in range(1, len(values)):
            values[i].set_previous(values[i-1])

    def __repr__(self):

        if self.mode == 'seq':
            return self.sequence_words()

        if self.mode == 'aggregate':
            return self.basic_words()

    def sequence_words(self):

        parts = []
        for c in self.subchunks:
            parts.append(repr(c))

        tpl = ' and '.join(parts)
        return tpl

    def dumbchunk(self):

        chunk_len = 6
        parts = []
        for i in range(0, len(self.subchunks), chunk_len):
            bigchunk = MultiChunk(self.subchunks[i:i+chunk_len], mode='aggregate')
            parts.append(bigchunk)

        self.subchunks = parts


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
        maxs = [c.max for c in self.subchunks]
        return max(maxs)

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













def score_max(option):

    errors = []

    for part in option:
        c = Chunk(option)
        maxs = c.maxs()
        c_max = c.max()

        errors += [c_max - cmax for cmax in maxs]

    goods = [1 - e for e in errors]
    good = reduce(operator.mul(goods))
    error = 1 - good


#
#
#     def dumbchunk(self):
#         dumbchunk_count = 4
#
#         chunked = []
#
#         length = len(self.raw_chunks)
#         if length > dumbchunk_count:
#             sublength = int(length / dumbchunk_count)
#             for i in range(0, length, sublength):
#                 subchunk = chunk(self.raw_chunks[i:i+sublength])
#                 chunked.append(subchunk)
#
#         self.chunks = chunked
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
#
#
#
#
#
# class TinyChunk(Chunk):
#     '''
#     A 'leaf' chunk with actual data in it
#     '''
#
#     def __init__(self, values):
#         try:
#             start, end, the_min, the_max = values
#
#         except:
#             print(values)
#             raise
#         self.values = values
#         self.start = start
#         self.end = end
#         self.min = the_min
#         self.max = the_max
#
#     def __repr__(self):
#
#         show = "Hours %s to %s: Min %s to Max %s" % (self.values)
#         return show
#
#     def starts(self):
#         return [self.start]
#
#     def ends(self):
#         return [self.end]
#
#     def mins(self):
#         return [self.min]
#
#     def maxs(self):
#         return [self.max]
