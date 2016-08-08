#!/usr/bin/env python

import argparse
import sys
from utils import dashdelim, parsematrix
from utils_15 import Graph
from math import log10

# Parse command line arguments
def parse_cmdline_params(arg_list=None):
    """Parses commandline arguments.
    """

    description = "Viterbi"

    #Create instance of ArgumentParser
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-f", "--file", required=True, type=argparse.FileType('r'),
                        help="file with data")

    # Parse options
    opts = parser.parse_args(args=arg_list)

    return opts


def main(args):

    #Setup
    opts = parse_cmdline_params(args[1:])

    # Break up file into sections
    sections = dashdelim(opts.file.readlines())

    output_str = sections[0][0].rstrip()
    output_alpha = sections[1][0].rstrip().split()

    states = sections[2][0].rstrip().split()
    trans_matrix = parsematrix(sections[3])
    emiss_matrix = parsematrix(sections[4])

    # We need to set up some nodes and edges!
    # edge spec from problem 1-5 is start node, end node, weight.
    # weight = (trans_prob)(emiss_prob|state)
    edges = []
    for i in range(len(output_str)):
        emitted = output_str[i]
        statenumstr = str(i+1)
        if i == 0:
            # Set up source
            # Weights are simply the probability that each
            # state emits the emitted signal
            # Use logs so we can keep the scoring the same in DAG
            for state in states:
                node_name = state + statenumstr
                edges.append(['source', node_name, log10(emiss_matrix[state][emitted])])
            continue

        # We have to establish an edge from each state to each state
        for start_state in states:
            start_node = start_state + str(i)
            for end_state in states:
                end_node = end_state + statenumstr
                edges.append([start_node, end_node,
                              log10(trans_matrix[start_state][end_state] * emiss_matrix[end_state][emitted])])
    # We need a sink
    for state in states:
        # The last statenumstr is the start node
        edges.append([state + statenumstr, 'sink', 0])


    print edges
    for edge in edges:
        print edge

    G = Graph(edges)

    G.calculate_path_information('source')

    path_nodes = G.backtrack_longest_path('source', 'sink')

    path_nodes = path_nodes[1:-1]
    print "".join([pn[0] for pn in path_nodes])

if __name__ == "__main__":
    main(sys.argv)

