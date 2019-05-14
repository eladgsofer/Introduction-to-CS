import Huffman_code_interface
from binary_tree import Node
import os
from os import path
import math



class HuffmanCoding(Huffman_code_interface.HuffmanCoding):
    CURR_PATH = path.dirname(__file__)
    TEST_PATH = path.join(CURR_PATH, 'test')


    def __init__(self, input_file_path):
        ''' init method for class HuffmanCoding.
        input_file_path is a string containing the path to a file which needs to be compressed
        '''
        self.input_file_path = input_file_path
        self.coding_dictionary = dict()
        self.freq_dict = dict()
        self.compressed_file_path = path.join(self.TEST_PATH)

        self.__init_dict()
        self.tree = self.build_hoff_tree()
        self.build_code_dict()


    def __init_dict(self):
        mode = 'r' if 'txt' in self.input_file_path else 'rb'
        with open(self.input_file_path, mode=mode) as fd:
            data = fd.read()
        for ch in data:
            if ch not in self.freq_dict:
                self.freq_dict[ch] = 0
            self.freq_dict[ch] += 1


    def build_hoff_tree(self):
        #TODO build a tree instead of using a list
        queue = [Node(freq=freq, char=ch) for ch, freq in self.freq_dict.items()]
        queue = sorted(queue, key=lambda n: n, reverse=True)
        while len(queue)!=1:
            a, b  = queue.pop(), queue.pop()
            node = Node(a.freq + b.freq, char=None)
            node.left, node.right = a, b
            queue.append(node)
            queue = sorted(queue, key=lambda n: n, reverse=True)
        return queue[0]

    def build_code_dict(self):
        for freq in self.freq_dict.keys():
            self.coding_dictionary[freq] = self.tree.get_code(freq)

    def decompress_file(self, input_file_path):
        ''' This method decompresses a previously compressed file.
        Input: input_file_path - path to compressed file.
        Output path to decompressed file (string).
        '''
        return path.join(self.compressed_file_path, 'f_test')

    def calculate_entropy(self):
        ''' This method calculates the entropy associated with the distribution
         of symbols in a previously compressed file.
        Input: None.
        Output: entropy (float).
        '''
        raise NotImplementedError




if __name__ == '__main__':  # You should keep this line for our auto-grading code.
    HuffmanCoding(os.path.join(HuffmanCoding.TEST_PATH, 'Lipsum.txt'))
