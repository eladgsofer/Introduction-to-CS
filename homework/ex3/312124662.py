__author__ = 'Elad Sofer <elad.sofe@post.bgu.ac.il>'


import Huffman_code_interface
import math
import os
from functools import total_ordering
from enum import Enum

class DataMode(Enum):
    TEXT = 't'
    BINARY = 'b'

class FilePrefix(Enum):
    TEXT = 'txt'
    BINARY = 'binary'


@total_ordering
class HeapBinaryNode(object):
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

    def assign_codes(self,coding_dict, code_prefix=''):

        if self.char is not None:
            coding_dict[self.char] = code_prefix
        if self.left is not None:
            self.left.assign_codes(coding_dict, code_prefix + '0')
        if self.right is not None:
            self.right.assign_codes(coding_dict, code_prefix + '1')

    def retrieve_data(self, byte_string, mode):
        data_buffer = '' if mode == DataMode.TEXT.value else bytearray()
        curr_node = self
        for b in byte_string:
            if b == '1':
                curr_node = curr_node.right
            else:
                curr_node = curr_node.left
            if curr_node.char is not None:
                if mode == DataMode.TEXT.value:
                    data_buffer += curr_node.char
                else:
                    data_buffer.append(curr_node.char)
                curr_node = self
        return data_buffer


class HuffmanCoding(Huffman_code_interface.HuffmanCoding):

    BYTE_LENGTH = 8


    def __init__(self, input_file_path):
        ''' init method for class HuffmanCoding.
        input_file_path is a string containing the path to a file which needs to be compressed
        '''
        self.input_file_path = input_file_path
        self.file_path, self.extension = os.path.splitext(input_file_path)
        self.mode = DataMode.TEXT.value if FilePrefix.TEXT.value in input_file_path else DataMode.BINARY.value

        self.compressed_file_path =  self.file_path + '_cmp.bin'

        self.coding_dictionary = dict()
        self.freq_dict = dict()
        self.tree = None
        self.data = None

        self.__init_dict()
        self.__init_bin_tree()
        self.tree.assign_codes(self.coding_dictionary)
        # Start to compress the file
        self.compress_file()


    def __init_dict(self):
        kwargs =  {'mode': 'r' + self.mode}
        if self.mode == DataMode.TEXT.value:
            kwargs['newline'] = '\n'

        with open(self.input_file_path, **kwargs) as fd:
            self.data = fd.read()
        for ch in self.data:
            if ch not in self.freq_dict:
                self.freq_dict[ch] = 1
            else:
                self.freq_dict[ch] += 1


    def __init_bin_tree(self):
        #TODO build a tree instead of using a list - nlogn
        queue = sorted([HeapBinaryNode(freq=freq, char=ch)
                 for ch, freq in self.freq_dict.items()], reverse=True)
        while len(queue)!=1:
            a, b  = queue.pop(), queue.pop()
            node = HeapBinaryNode(a.freq + b.freq, char=None)
            node.left, node.right = a, b
            queue.append(node)
            queue = sorted(queue, reverse=True)
        self.tree = queue[0]

    def compress_file(self):
        """
        This method compress a file by huffman code
        :return:
        """
        byte_string = ''
        b_array = bytearray()

        for ch in self.data:
            byte_string += self.coding_dictionary[ch]

        padding_offset = len(byte_string) % self.BYTE_LENGTH
        if padding_offset != 0:
            padding_length = self.BYTE_LENGTH-padding_offset
        else:
            padding_length = 0
        byte_string += '0'*padding_length
        b_array.extend(bytes([padding_length]))


        for i in range(0, len(byte_string), self.BYTE_LENGTH):
            b_array.append(int(byte_string[i:i+self.BYTE_LENGTH], 2))

        self.delete_prev_file(self.compressed_file_path)
        with open(self.compressed_file_path, mode='wb') as fd:
            fd.write(b_array)

    @staticmethod
    def delete_prev_file(f):
        if os.path.exists(f):
            os.remove(f)


    def decompress_file(self, input_file_path):
        ''' This method decompresses a previously compressed file.
        Input: input_file_path - path to compressed file.
        Output path to decompressed file (string).
        '''
        dcmp_raw_data = ""
        dcmp_output_file = self.file_path + '_dcmp' + self.extension
        with open(input_file_path, mode='rb') as fd:
            byte_stream = bytearray(fd.read())

        padding_offset = byte_stream.pop(0)
        padded_lsb = bin(byte_stream.pop())[2:].rjust(self.BYTE_LENGTH, '0')
        padded_lsb = padded_lsb[:self.BYTE_LENGTH - padding_offset]
        for byte in byte_stream:
            dcmp_raw_data += bin(byte)[2:].rjust(self.BYTE_LENGTH, '0')
        dcmp_raw_data +=padded_lsb
        dcmp_text = self.tree.retrieve_data(dcmp_raw_data, self.mode)

        self.delete_prev_file(dcmp_output_file)
        with open(dcmp_output_file, mode='w' + self.mode) as fd:
            fd.write(dcmp_text)

        return dcmp_output_file


    def calculate_entropy(self):
        ''' This method calculates the entropy associated with the distribution
         of symbols in a previously compressed file.
        Input: None.
        Output: entropy (float).
        '''
        entropy = 0
        total_symobols = self.tree.freq
        for freq in self.freq_dict.values():
            p = freq/total_symobols
            entropy-=p*math.log2(p)
        return entropy
