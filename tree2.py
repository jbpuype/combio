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
    def setlabel(self,lab):
        self.label = lab

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

allskv=[]
def small_parsimony(tree, alphabet):
    toppen = []
    for v in tree:
        toppen.append(v)
    t = 0
    numb= 10
    s=[]
    for i in range(numb):
        small_parsimony_impl(tree, alphabet, i)
    for i in toppen:
        k=''
        for j in range(numb):
            kk={}
            for a in alphabet:
                kk[a]=allskv[j][a][i]
            l = min(kk, key=kk.get)
            k=k + l
        s.append(k)
    for i,j in zip(tree, s):
        i.setlabel(j)

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
        for v in done.keys():
            if not done[v] and done[v.treel()] and done[v.treer()]:
                d.add(v)
    out = {}
    allskv.append(s)
    for k in alphabet:
        out[k] = 0
    for (k, sk) in s.items():
            out[k] += sum(filter(lambda n: n < math.inf, sk.values()))
    mini = min(out.items(), key=lambda x: x[1])
    return mini


def delta(i, j):
    if i != j:
        return 1
    return 0

tree = Tree.loadtxt("tree.txt")
print(small_parsimony(tree, 'ACGT'))
