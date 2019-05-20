from functools import total_ordering


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
        if self.char:
            return 'ch:{0}|freq{1}'.format(self.char, self.freq)
        return '{0}<<(({1}))>>{2}'.format(str(self.left.freq),str(self.freq), str(self.right.freq))

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

    def assign_codes(self,coding_dict, code_prefix=""):

        if self.char is not None:
            coding_dict[self.char] = code_prefix
        if self.left is not None:
            self.left.assign_codes(coding_dict, code_prefix + "0")
        if self.right is not None:
            self.right.assign_codes(coding_dict, code_prefix + "1")

    def retrieve_data(self, byte_string, mode):
        data_buffer = "" if mode == 't' else bytearray()
        curr_node = self
        for b in byte_string:
            if b == "1":
                curr_node = curr_node.right
            else:
                curr_node = curr_node.left
            if curr_node.char is not None:
                if mode == 't':
                    data_buffer += curr_node.char
                else:
                    data_buffer.append(curr_node.char)
                curr_node = self
        return data_buffer


if __name__ == '__main__':
    root = Node(5)
    root.insert(Node(6,'B'))
    root.insert(Node(7,'C'))
    root.insert(Node(3,'D'))
    # d = {}
    # root.assign_codes(d)