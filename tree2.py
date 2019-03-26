import re
from itertools import chain
import math


class Tree:
    def __init__(self, name=None, label=None, lt=None, lw=None, rt=None, rw=None):
        self.__name = name
        self.__label = label
        self.__lst = lt
        self.__lw = lw
        self.__rst = rt
        self.__rw = rw

    def label(self):
        return self.__label

    def treel(self):
        return self.__lst

    def treer(self):
        return self.__rst

    def name(self):
        return self.__name

    def setlabel(self, lab):
        self.__label = lab

    def set_lw(self, new_lw):
        self.__lw = new_lw

    def set_rw(self, new_rw):
        self.__rw = new_rw

    def __repr__(self):
        out = 'Tree('
        if self.__label is not None:
            out += repr(self.__label)
        if self.__lst is not None:
            out += ', lt=' + repr(self.__lst)
        if self.__lw is not None:
            out += ', lw=' + repr(self.__lw)
        if self.__rst is not None:
            out += ', rt=' + repr(self.__rst)
        if self.__rw is not None:
            out += ', rw=' + repr(self.__rw)
        return out + ')'

    def __next__(self):
        return self

    def __iter__(self):
        it = iter([self])
        if self.__lst is not None:
            it = chain(it, self.__lst)
        if self.__rst is not None:
            it = chain(it, self.__rst)
        return it

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))

    @staticmethod
    def loadtxt(file):
        with open(file, 'r') as f:
            lines = f.read().splitlines()
            nodes = []
            for line in lines:
                split = line.split("->")
                nodes.append((int(split[0]), split[1]))
            return Tree.build_sub_tree(0, nodes)

    @staticmethod
    def build_sub_tree(level, lst):
        sublst = list(filter(lambda p: p[0] == level, lst))
        if re.match(r'\d+', sublst[0][1]):
            lft = Tree.build_sub_tree(int(sublst[0][1]), lst)
        else:
            lft = Tree(label=sublst[0][1])
        if len(sublst) == 2:
            if re.match(r'\d+', sublst[1][1]):
                rght = Tree.build_sub_tree(int(sublst[1][1]), lst)
            else:
                rght = Tree(label=sublst[1][1])
        else:
            rght = None
        return Tree(label=level, lt=lft, rt=rght)


allskv = []


def hamDist(x, y):
    return str(sum([1 for f in zip(x, y) if f[0] != f[1]]))


def small_parsimony(tree, alphabet):
    toppen = list(tree)
    numb = max([len(repr(v.label())) for v in tree])-2
    t = 0
    s = []
    for i in range(numb):
        small_parsimony_impl(tree, alphabet, i)
    for i in toppen:
        k = ''
        for j in range(numb):
            kk = {}
            for a in alphabet:
                kk[a] = allskv[j][a][i]
            l = min(kk, key=kk.get)
            k = k + l
        s.append(k)
    for i, j in zip(tree, s):
        i.setlabel(j)
    for v in tree:
        if v.treel() is not None:
            v.set_lw(hamDist(v.label(), v.treel().label()))
        if v.treer() is not None:
            v.set_rw(hamDist(v.label(), v.treer().label()))
    return tree


def small_parsimony_impl(tree, alphabet, index):
    alphabet = list(alphabet)
    s = {}
    for k in alphabet:
        s[k] = {}
    done = {}
    for v in tree:
        done[v] = False
        if v.treel() is None:
            done[v] = True
            for k in alphabet:
                if list(v.label())[index] == k:
                    s[k][v] = 0
                else:
                    s[k][v] = math.inf
    d = set()
    for v in done.keys():
        if not done[v] and done[v.treel()] and done[v.treer()]:
            d.add(v)
    while len(d) > 0:
        v = d.pop()
        done[v] = True
        for k in alphabet:
            min_daughter = math.inf
            for i in alphabet:
                min_daughter = min(min_daughter, s[i][v.treel()] + delta(i, k))
            min_son = math.inf
            for j in alphabet:
                min_son = min(min_son, s[j][v.treer()] + delta(j, k))
            s[k][v] = min_daughter + min_son
        for w in done.keys():
            if not done[w] and done[w.treel()] and done[w.treer()]:
                d.add(w)
    return {v: min(alphabet, key=lambda k: s[k][v]) for v in tree}


def delta(i, j):
    if i != j:
        return 1
    return 0


tree = Tree.loadtxt("tree.txt")
print(small_parsimony(tree, 'ACGT'))
