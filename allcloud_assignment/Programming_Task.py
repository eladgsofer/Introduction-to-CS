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

    def start(self):
        """
        Main function which starts the tool.
        print the number of matches
        """
        ann_occurrences = dict.fromkeys(self.ann_dict.keys(), 0)
        for label, regex_list in self.ann_dict.items():
            for r_pattern in regex_list:
                r_pattern = str(r_pattern)
                try:
                    re_matches = re.findall(r_pattern, self.data)
                except Exception:
                    print "Regex syntax error, check the config file"
                    raise

                ann_occurrences[label] += len(re_matches)

        print '\n{0}\n\n{1}'.format('Label occurrences:', ann_occurrences)

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
