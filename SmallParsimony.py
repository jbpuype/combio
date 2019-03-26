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


def hamDist(x, y):
    count = 0
    for xx, yy in zip(x, y):
        if xx != yy:
            count += 1
    return str(count)


def SmallParsimony(T, Character):
    alphabet = ['A','C','T','G']
    skv={}
    done = {}
    for v in Tree.loadtxt("tree.txt"):
        done[v]=False
        if v.treel() == None:
            done[v]=True
            for k in alphabet:
                if v.lab()== k:
                    skv[(k,v)]= 0
                else:
                    skv[(k,v)]=math.inf
    d = set()
    for v in done.keys():
        if done[v]==False:
            if done[v.treel()] ==True:
                d.add(v)
    while len(d)>0:
        for v in d:
            done[v]=True
            for k in alphabet:
                minD= math.inf
                for i in alphabet:
                    tussenSom = skv[(i,v.treel())]+delta(i,k)
                    if tussenSom <minD:
                        minD= tussenSom
                minZ =math.inf
                for i in alphabet:
                    tussenSom = skv[(i,v.treer())]+delta(i,k)
                    if tussenSom <minZ:
                        minZ= tussenSom
                skv[(k,v)]= minD+minZ
        d = set()
        for v in done.keys():
            if done[v] == False:
                if done[v.treel()] == True:
                    d.add(v)
    return skv


def delta(i,j):
    if i==j:
        return 1
    return 0
tree = Tree.loadtxt("tree.txt")
Character=[]
for t in tree:
    Character.append(t)
print(SmallParsimony(tree, 'ACGT'))
