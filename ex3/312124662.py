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
        self.mode = 'txt' if 'txt' in input_file_path else 'bin'
        # self.input_file_dir = path.join(self.TEST_PATH, input_file_path)

        self.compressed_file_path = input_file_path + '.cmp'
        # self.compressed_file_path = path.join(self.TEST_PATH,self.compressed_file_name)

        self.coding_dictionary = dict()
        self.freq_dict = dict()
        self.tree = None
        self.data = None

        self.__init_dict()
        self.__init_bin_tree()
        self.tree.assign_codes(self.coding_dictionary)
        self.compress_file()


    def __init_dict(self):
        mode = 'rb' if self.mode == 'bin' else 'rt'
        with open(self.input_file_path, mode=mode) as fd:
            self.data = fd.read()
        for ch in self.data:
            if ch not in self.freq_dict:
                self.freq_dict[ch] = 1
            else:
                self.freq_dict[ch] += 1


    def __init_bin_tree(self):
        #TODO build a tree instead of using a list
        queue = [Node(freq=freq, char=ch) for ch, freq in self.freq_dict.items()]
        queue = sorted(queue, key=lambda n: n, reverse=True)
        while len(queue)!=1:
            a, b  = queue.pop(), queue.pop()
            node = Node(a.freq + b.freq, char=None)
            node.left, node.right = a, b
            queue.append(node)
            queue = sorted(queue, key=lambda n: n, reverse=True)
        self.tree = queue[0]

    def compress_file(self):
        byte_string = ""
        b_array = bytearray()

        for ch in self.data:
            byte_string = '{0}{1}'.format(byte_string, self.coding_dictionary[ch])

        padding_offset = len(byte_string) % 8
        byte_string = '{0}{1}'.format(byte_string, "0"*padding_offset)

        b_array.extend(bytes([padding_offset]))

        for i in range(0, len(byte_string), 8):
            b_array.extend(int(byte_string[i:i+8], 2).to_bytes(1, byteorder='big'))

        with open(self.compressed_file_path, mode='wb') as fd:
            fd.write(b_array)

    def decompress_file(self, input_file_path):
        ''' This method decompresses a previously compressed file.
        Input: input_file_path - path to compressed file.
        Output path to decompressed file (string).
        '''
        output = input_file_path + '.dcmp'
        with open(input_file_path, mode='rb') as fd:
            binary_data = fd.read()

        data = self.tree.decode(binary_data)
        w_mode =  'wt' if 'txt' in input_file_path else 'wb'
        with open (output, mode=w_mode) as fd:
            fd.write(data)
        return output


    def calculate_entropy(self):
        ''' This method calculates the entropy associated with the distribution
         of symbols in a previously compressed file.
        Input: None.
        Output: entropy (float).
        '''
        raise NotImplementedError




if __name__ == '__main__':  # You should keep this line for our auto-grading code.
    HuffmanCoding('Lipsum.txt')
