import re
from itertools import chain
import math


class Tree:
    def __init__(self, label=None, lt=None, lw=None, rt=None, rw=None):
        self.__label = label
        self.__lst = lt
        self.__lw = lw
        self.__rst = rt
        self.__rw = rw

    def label(self):
        return self.__label

    def set_label(self, new_label):
        self.__label = new_label

    def set_lw(self, new_lw):
        self.__lw = new_lw

    def set_rw(self, new_rw):
        self.__rw = new_rw

    def treel(self):
        return self.__lst

    def treer(self):
        return self.__rst

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


def hamDist(x, y):
    count = 0
    for xx, yy in zip(x, y):
        if xx != yy:
            count += 1
    return str(count)


def small_parsimony(tree, alphabet):
    from functools import reduce
    vmap = {v: [] for v in tree}
    for i in range(10):
        res = small_parsimony_impl(tree, alphabet, i)
        for x in res:
            vmap[x].append(res[x])
    for v in tree:
        v.set_label(reduce((lambda x, y: x + y), vmap[v]))
    for v in tree:
        if v.treel() is not None:
            v.set_lw(hamDist(v.label(), v.treel().label()))
        if v.treer() is not None:
            v.set_rw(hamDist(v.label(), v.treer().label()))
    return tree


def small_parsimony_impl(tree, alphabet, index):
    alphabet = list(alphabet)
    s = {k: {} for k in alphabet}
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
        if not done[v] and done[v.treel()]:
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
    all_min_vals = {v: all_min(alphabet, key=lambda k: s[k][v]) for v in tree}
    min_root=math.inf
    for k in alphabet:
        val =s[k][tree]
        if val <min_root:
            val=min_root
    assigned = {}
    assigned[tree] = min_root
    assign_values(min_root,tree,all_min_vals,assigned)
    return assigned


def assign_values(parent_assign, tree, min_vals, assigned):
    if tree is None:
        return assigned
    if parent_assign in min_vals[tree]:
        assigned[tree] = parent_assign
        a = parent_assign
    else:
        a = min_vals[tree].pop()
        assigned[tree] = a
    return {**assign_values(a, tree.treel(), min_vals, assigned), **assign_values(a, tree.treer(), min_vals, assigned)}



def all_min(o, key):
    min_value = min(o, key=key)
    return list(filter(lambda x: key(x) == key(min_value), o))


def delta(i, j):
    if i != j:
        return 1
    return 0


tree = Tree.loadtxt("tree.txt")
# Character = []
# for t in tree:
#     Character.append(t)
print(small_parsimony(tree, 'ACGT'))

Tree('label')
