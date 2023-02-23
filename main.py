# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Attribute:
    name = ""

    def __init__(self, n):
        self.name = n

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def print(self):
        return self.name


class Group:
    attributes = None

    def __init__(self):
        self.attributes = set()


    def __eq__(self, other):
        return self.attributes == other.attributes

    def __hash__(self):
        hash_ = 0
        for a in self.attributes:
            hash_ = hash_ ^ hash(a)
        return hash_

    def add(self, attribute):
        self.attributes.add(attribute)

    def union(self, group):
        union = set()
        for x in self.attributes:
            union.add(x)
        for x in group.attributes:
            union.add(x)
        g = Group()
        g.attributes = union
        return g

    def intersection(self, group):
        intersection = set()
        for x in self.attributes:
            for y in group.attributes:
                if x.name == y.name:
                    intersection.add(x)
        g = Group()
        g.attributes = intersection
        return g

    def print(self):
        s = "{"
        for x in self.attributes:
            s += x.print()
            s += ','
        if len(self.attributes)!=0:
            s = s[0:len(s) - 1]
        s += "}"
        return s


class FD:
    left_group = None
    right_group = None

    def __init__(self, left, right):
        self.left_group = left
        self.right_group = right

    def closure(self, group):
        if self.left_group.intersection(group) == self.left_group:
            return group.union(self.right_group)
        return group

    def print(self):
        return self.left_group.print()+"->"+self.right_group.print()

def subgroups(group):
    # returns a set of groups
    s = set()
    ats = list(group.attributes)
    n = 2**len(ats)
    for i in range(n):
        g = Group()
        for j in range(len(ats)):
            if (1<<j & i) != 0:
                g.add(Attribute(ats[j].name))
        s.add(g)

    return s


def apply_FDs(group, FDs):
    while True:
        i = len(group.attributes)
        for fd in FDs:
            group = fd.closure(group)
        if i == len(group.attributes):
            break
    return group


def main():
    f = open("./input.txt", "r")
    input_file = f.readlines()
    f.close()
    atbs = Group()  # all possible attributes
    fds = list()
    for x in input_file:
        s = x.split()
        if s.__contains__("->"):  # functional dependency
            left = Group()
            right = Group()
            temp = left
            for t in s:
                if t == "->":
                    temp = right
                    continue
                temp.add(Attribute(t))
            fds.append(FD(left, right))
            pass
        else:  # list of all attributes
            for t in s:
                atbs.add(Attribute(t))

    print("Attributes:")
    print(atbs.print())
    print("FDs:")
    for fd in fds:
        print(fd.print())
    sg = subgroups(atbs)

    keys = set()
    for t in sg:
        if apply_FDs(t,fds) == atbs:
            keys.add(t)

    candidate_keys = set()
    for t in keys:
        ct = 0
        for u in keys:
            if t.union(u) == t:
                ct+=1
        if ct==1:
            candidate_keys.add(t)

    print("candidate keys are:")
    for t in candidate_keys:
        print(t.print())




if __name__ == '__main__':
    main()
