from collections.abc import Iterable
from joblib import Parallel, delayed

import iteration_utilities
from forbiddenfruit import curse


class ImkCollections:

    def __call__(self, o):
        assert isinstance(o, list) or isinstance(o, tuple)
        return ImkList(o)

    def uniq(self, iterable, key=None):
        return list(iteration_utilities.unique_everseen(iterable, key))

    def flatten(self, *o):
        items = []

        def visit(at):
            if isinstance(at, str):
                items.append(at)
            elif isinstance(at, bytes):
                items.append(at)
            elif isinstance(at, Iterable):
                for a in at:
                    visit(a)
            else:
                items.append(at)

        visit(o)
        return items

    def grouped(self, ll: list, group_size):
        return [ll[i:i + 10] for i in range(0, len(ll), group_size)]

    def wk(self, c, fn):
        if isinstance(c, list):
            return [self.wk(o, fn) for o in c]
        elif isinstance(c, dict):
            return dict((k, self.wk(c[k], fn)) for k in c)
        else:
            return fn(c)


class ImkList(list):

    @property
    def single(self):
        assert len(self) == 1
        return self[0]

    def m(self, fn) -> 'ImkList':
        return ImkList([fn(o) for o in self])

    def mn(self, fn) -> 'ImkList':
        return ImkList([fn(o) for o in self if fn(o) is not None])

    def f(self, fn):
        return ImkList([o for o in self if fn(o)])

    def ff(self, fn, opt: bool = False):
        for o in self:
            if fn(o):
                return o
        if opt:
            return None
        else:
            raise Exception('ff: no match')

    def fl(self):
        """lists the items in the list recursively"""
        items: list = []

        def visit(at):
            # NOTE: early returns needed for str and bytes
            # because they are iterable
            if isinstance(at, str):
                items.append(at)
            elif isinstance(at, bytes):
                items.append(at)
            elif isinstance(at, Iterable):
                for a in at:
                    visit(a)
            else:
                items.append(at)

        visit(self)
        return items

    def exp(self, fn) -> 'ImkList':
        """maps the list and flattens the result"""
        ys = []
        for x in self:
            ys.extend(fn(x))
        return ImkList(ys)

    def par(self, n=10):
        par_list = ImkParallelList(self)
        par_list.n = n
        return par_list

    def zis(self) -> 'ImkList':
        """zips the list with an index string 0000 - 9999"""
        assert len(self) < 10000
        return ImkList(zip(self, [f'0000{i}'[-4:] for i in range(len(self))]))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return ImkList(super().__getitem__(item))
        else:
            return super().__getitem__(item)

    @property
    def one(self):
        assert len(self) == 1
        return self[0]


class ImkParallelList(list):
    n: int = 10

    def m(self, fn) -> 'ImkList':
        return ImkList(Parallel(n_jobs=self.n)(delayed(fn)(item) for item in self))


curse(list, 'm', ImkList.m)
curse(list, 'mn', ImkList.mn)
curse(list, 'f', ImkList.f)
curse(list, 'ff', ImkList.ff)
curse(list, 'fl', ImkList.fl)
curse(list, 'exp', ImkList.exp)
curse(list, 'zis', ImkList.zis)
curse(list, 'one', ImkList.one)
curse(list, 'par', ImkList.par)
