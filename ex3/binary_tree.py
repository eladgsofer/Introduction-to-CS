from functools import total_ordering


class BinaryTree():
    def __init__(self, root_node):
        self.root = root_node
        self.coding_dict = {}

@total_ordering
class Node(object):
    def __init__(self, freq, char=None, right=None, left=None):
        self.freq = freq
        self.char  = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return '{0}<<(({1}))>>{2}'.format(str(self.left.freq),str(self.freq), str(self.right.freq))

    def __gt__(self, other):
        return self.freq > other.freq

    def insert(self, node):

        if node > self:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)
        if node < self:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)

    def assign_codes(self,coding_dict, prefix=""):

        if self.char:
            coding_dict[self.char] = prefix
        if self.left is not None:
            self.left.assign_codes(coding_dict, "0" + prefix)
        if self.right is not None:
            self.right.assign_codes(coding_dict, "1" + prefix)




if __name__ == '__main__':
    root = Node(5)
    root.insert(Node(6,'B'))
    root.insert(Node(7,'C'))
    root.insert(Node(3,'D'))
    d = {}
    root.assign_codes(d)