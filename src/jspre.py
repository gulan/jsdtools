#!python

import argparse
import sys
from jsdtools.regex_syntax.parse_re import RegexParser

def display_tree(r, subs):
    p = RegexParser()
    ast = p.parse(r)
    ast.relabel(subs)
    for (level, _, node, name, _) in ast.walk():
        if node == 'lit':
            print('    ' * level, name)
        else:
            print('    ' * level, node, name+':')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--labels', default='')
    parser.add_argument('regex')
    args = parser.parse_args()
    labels = args.labels.split(',')
    if labels[0] == '':
        subs = dict()
    else:
        keys = ["_%d" % i for i in range(1,len(labels)+1)]
        subs = dict(zip(keys, labels))
    display_tree(args.regex, subs)
