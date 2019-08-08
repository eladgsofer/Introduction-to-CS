__author__ = 'Elad Sofer <eladsofe@post.bgu.ac.il>'

import json
import os
import re

from argparse import ArgumentParser


class AllCloudParsingTool(object):
    """
    Exercise AllCloud
    """

    def __init__(self, data_fname, annotation_fname):
        self.data_fname = data_fname
        self.ann_fname = annotation_fname
        self.data = None
        self.ann_dict = None
        self.__config_load()

    def __config_load(self):
        with open(self.data_fname) as fd:
            self.data = fd.read()

        with open(self.ann_fname) as fd:
            self.ann_dict = json.load(fd)

    @staticmethod
    def verify_regex_match(match):
        if match:
            if match[0] == "":
                return False
            return True

    def start(self):
        """
        Main function which starts the tool.
        print the number of matches
        """
        ann_freq_dict = dict.fromkeys(self.ann_dict.keys(), 0)
        for label, regex_dict in self.ann_dict.items():
            string_lst = regex_dict["strings"]
            regex_lst = regex_dict["regex"]
            for s in string_lst:
                # In case a word - determine a whole word regex boundaries
                str_matches = re.findall(r'\b' + str(s) + r'\b', self.data)

                if self.verify_regex_match(str_matches):
                    ann_freq_dict[label] += len(str_matches)

            for r in regex_lst:
                # In case a generic regex - simply pass the regex.
                regex_matches = re.findall(str(r), self.data)

                if self.verify_regex_match(regex_matches):
                    ann_freq_dict[label] += len(regex_matches)

        print '\n{0}\n\n{1}'.format('Label occurrences:', ann_freq_dict)

if __name__ == '__main__':
    parser = ArgumentParser("Programming Task - AllCloud")
    parser.add_argument('--data-file', action='store', dest='data_fname',
                        type=str,
                        help='Enter data file name - Relative path to curr_dir')

    parser.add_argument('--annotation-file', action='store', type=str,
                        dest='annotation_fname',
                        help='Enter annotation JSON file name '
                             '- Relative path to curr_dir')
    args = parser.parse_args()
    if os.path.exists(args.data_fname) and os.path.exists(
            args.annotation_fname):
        tool = AllCloudParsingTool(args.data_fname, args.annotation_fname)
        tool.start()
    else:
        raise IOError("One of the configuraton files doesn't exist!")
