from plotly.graph_objs import Scatter, Figure, Layout


def chunk(values):

    # List of Chunks
    if isinstance(values[0], Chunk):
        return ChunkyChunk(values)

    # List of actual values
    if not isinstance(values, Chunk):
        return TinyChunk(values)

    # A chunk of some kind
    return ChunkyChunk(values)


class Chunk():
    '''
    A chunk comprises a list of sub-chunks
    '''

    def fig(self):

        starts = self.starts()
        maxs = self.maxs()

        trace = Scatter(x=starts, y=maxs)
        layout = Layout(
            xaxis=dict(range=[0, 24]),
            yaxis=dict(range=[5, 18])
        )
        fig = Figure(data=[trace], layout=layout)
        return fig


class ChunkyChunk(Chunk):
    '''
    An aggregation of other chunks.
    '''

    def __init__(self, chunks):
        self.chunks = chunks  # all the little chunks
        self.chunked = chunks  # one big chunk

    @property
    def min(self):
        return min([c.min for c in self.chunks])

    @property
    def max(self):
        return max([c.max for c in self.chunks])

    @property
    def start(self):
        return min([c.start for c in self.chunks])

    @property
    def end(self):
        return max([c.end for c in self.chunks])

    def starts(self):
        return [c.start for c in self.chunked]

    def maxs(self):
        return [c.max for c in self.chunked]

    def dumbchunk(self):
        dumbchunk_count = 4

        chunked = []

        length = len(self.chunks)
        if length > dumbchunk_count:
            sublength = int(length / dumbchunk_count)
            for i in range(0, length, sublength):
                subchunk = chunk(self.chunks[i:i+sublength])
                chunked.append(subchunk)

        self.chunked = chunked





class TinyChunk(Chunk):
    '''
    A 'leaf' chunk with actual data in it
    '''

    def __init__(self, values):
        try:
            start, end, the_min, the_max = values

        except:
            print(values)
            raise
        self.values = values
        self.start = start
        self.end = end
        self.min = the_min
        self.max = the_max

    def __repr__(self):

        show = "Hours %s to %s: Min %s to Max %s" % (self.values)
        return show

    def starts(self):
        return [self.start]

    def ends(self):
        return [self.end]

    def mins(self):
        return [self.min]

    def maxs(self):
        return [self.max]
