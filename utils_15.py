#!/usr/bin/env python

import sys

def dp_change(amount, denominations):
    min_num_coins = [0]

    for incremental_amount in range(1,amount+1):
        min_num_coins.append(1e6)
        for d in denominations:
            if incremental_amount >= d:
                if min_num_coins[incremental_amount-d] + 1 < min_num_coins[incremental_amount]:
                    min_num_coins[incremental_amount] = min_num_coins[incremental_amount - d] + 1
    return min_num_coins[-1]


def generate_empty_2d_array(rows, cols):

    return [[0 for _ in range(cols)] for _ in range(rows)]


def ManhattanTourist(rows, cols, down_weights, right_weights):

    # Initialize the length storage
    path_lengths = generate_empty_2d_array(rows+1, cols+1)

    # Fill in the first row and column
    for i in range(1, rows+1):
        path_lengths[i][0] = path_lengths[i-1][0] + down_weights[i-1][0]

    for j in range(1, cols+1):
        path_lengths[0][j] = path_lengths[0][j-1] + right_weights[0][j-1]

    # Fill in the rest:
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            path_lengths[i][j] = max([path_lengths[i-1][j] + down_weights[i-1][j],
                                     path_lengths[i][j-1] + right_weights[i][j-1]])

    return path_lengths[rows][cols]


DOWN=1
RIGHT=2
DIAG=3
SOURCE=4

def LCSBacktrack(v, w):

    s = generate_empty_2d_array(len(v)+1, len(w)+1)
    b = generate_empty_2d_array(len(v)+1, len(w)+1)

    # Top row and left col are already zeros.
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):

            maxvals = [s[i-1][j], s[i][j-1], s[i-1][j-1] + 1 * (v[i-1] == w[j-1])]

            max_val = max(maxvals)
            max_index = maxvals.index(max_val)

            s[i][j] = max_val

            if max_index == 0:
                b[i][j] = DOWN
            elif max_index == 1:
                b[i][j] = RIGHT
            else:
                b[i][j] = DIAG

    return s, b


def LCSBacktrack2(v, w, score_matrix, indel_penalty):

    s = generate_empty_2d_array(len(v)+1, len(w)+1)
    b = generate_empty_2d_array(len(v)+1, len(w)+1)

    # Fill in the top row and left column with the indel penalties.
    for i in range(1, len(v)+1):
        s[i][0] = s[i-1][0] - indel_penalty
        b[i][0] = DOWN
    for j in range(1, len(w)+1):
        s[0][j] = s[0][j-1] - indel_penalty
        b[0][j] = RIGHT

    # Fill in remaining scores
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):

            inpath_scores = [s[i-1][j] - indel_penalty,
                             s[i][j-1] - indel_penalty,
                             s[i-1][j-1] + score_matrix[v[i-1], w[j-1]]]

            max_val = max(inpath_scores)
            max_index = inpath_scores.index(max_val)

            s[i][j] = max_val

            if max_index == 0:
                b[i][j] = DOWN
            elif max_index == 1:
                b[i][j] = RIGHT
            else:
                b[i][j] = DIAG

    return s, b

words = {DOWN: 'DOWN', RIGHT: 'RIGHT', DIAG: 'DIAG', SOURCE: 'SOURCE'}

def LCSBacktrack3(v, w, score_matrix, indel_penalty):

    s = generate_empty_2d_array(len(v)+1, len(w)+1)
    b = generate_empty_2d_array(len(v)+1, len(w)+1)

    # There is a connection between the source and every
    # other node, with weight zero.  This means that the
    # top row and left column are all zeros.

    # Fill in the top row and left column with the indel penalties.
    for i in range(1, len(v)+1):
        s[i][0] = 0
        b[i][0] = SOURCE
    for j in range(1, len(w)+1):
        s[0][j] = 0
        b[0][j] = SOURCE

    # Fill in remaining scores
    local_max = 0
    local_ij = (0, 0)
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):

            # Determine if the highest score is from
            # shortcut, indel, or diagonal
            inpath_scores = [0,
                             s[i-1][j] - indel_penalty,
                             s[i][j-1] - indel_penalty,
                             s[i-1][j-1] + score_matrix[v[i-1], w[j-1]]]

            max_val = max(inpath_scores)
            max_index = inpath_scores.index(max_val)

            s[i][j] = max_val

            if max_index == 0:
                b[i][j] = SOURCE
            elif max_index == 1:
                b[i][j] = DOWN
            elif max_index == 2:
                b[i][j] = RIGHT
            else:
                b[i][j] = DIAG

            # print "({}, {}) [{}, {}] {} {}: {} ({}, {}) = {}".format(i, j,
            #                                                   v[i-1], w[j-1],
            #                                                   words[b[i][j]],
            #                                                   s[i][j], str(inpath_scores),
            #                                                   i-1, j-1, s[i-1][j-1])

            if max_val > local_max:
                local_max = max_val
                local_ij = (i, j)

    # Override the last position to link to the max score in the array
    if local_max > s[len(v)][len(w)]:
        s[len(v)][len(w)] = local_max
        b[len(v)][len(w)] = local_ij

    return s, b


def LCSBacktrackOverlap(v, w):

    s = generate_empty_2d_array(len(v)+1, len(w)+1)
    b = generate_empty_2d_array(len(v)+1, len(w)+1)

    # The source can be any of the top or left col
    for i in range(1, len(v)+1):
        s[i][0] = 0
        b[i][0] = SOURCE
    for j in range(1, len(w)+1):
        s[0][j] = 0
        b[0][j] = SOURCE

    # Fill in remaining scores
    local_max = 0
    local_ij = (0, 0)
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):

            # Determine if the highest score is from
            # indel or diagonal
            diag_score = 1
            if v[i-1] != w[j-1]:
                diag_score = -2
            inpath_scores = [s[i-1][j] - 2,
                             s[i][j-1] - 2,
                             s[i-1][j-1] + diag_score]

            max_val = max(inpath_scores)
            max_index = inpath_scores.index(max_val)

            s[i][j] = max_val

            if max_index == 0:
                b[i][j] = DOWN
            elif max_index == 1:
                b[i][j] = RIGHT
            else:
                b[i][j] = DIAG

            # print "({}, {}) [{}, {}] {} {}: {} ({}, {}) = {}".format(i, j,
            #                                                   v[i-1], w[j-1],
            #                                                   words[b[i][j]],
            #                                                   s[i][j], str(inpath_scores),
            #                                                   i-1, j-1, s[i-1][j-1])

    edge_max = 0
    for i in range(1, len(v)+1):
        if s[i][len(w)] > edge_max:
            edge_max = s[i][len(w)]
            edge_ij = (i, len(w))
    for j in range(1, len(w)+1):
        if s[len(v)][j] > edge_max:
            edge_max = s[len(v)][j]
            edge_ij = (len(v), j)

    # Override the last position to link to the max score in the array
    if edge_max > s[len(v)][len(w)]:
        s[len(v)][len(w)] = edge_max
        b[len(v)][len(w)] = edge_ij

    return s, b



def LCSBacktrackED(v, w):

    s = generate_empty_2d_array(len(v)+1, len(w)+1)
    b = generate_empty_2d_array(len(v)+1, len(w)+1)

    # Fill in the top row and left column
    for i in range(1, len(v)+1):
        s[i][0] = s[i-1][0] - 1
        b[i][0] = DOWN
    for j in range(1, len(w)+1):
        s[0][j] = s[0][j-1] - 1
        b[0][j] = RIGHT

    # Fill in remaining scores
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):

            inpath_scores = [s[i-1][j] - 1,
                             s[i][j-1] - 1,
                             s[i-1][j-1] - (v[i-1] != w[j-1])]

            max_val = max(inpath_scores)
            max_index = inpath_scores.index(max_val)

            s[i][j] = max_val

            if max_index == 0:
                b[i][j] = DOWN
            elif max_index == 1:
                b[i][j] = RIGHT
            else:
                b[i][j] = DIAG

    return s, b

GAP_UNKNOWN = None
GAP_V_OPEN = 1
GAP_V_EXTEND = 2
GAP_V_CLOSE = 3
GAP_W_OPEN = 4
GAP_W_EXTEND = 5
GAP_W_CLOSE = 6
GAP_DIAG = 7
GAP_SOURCE = 8

def LCSBacktrackGAP(v, w, gapopen, gapextend, score_matrix):

    max_i = len(v) + 1
    max_j = len(w) + 1

    # Three node layers
    L = generate_empty_2d_array(max_i, max_j)
    M = generate_empty_2d_array(max_i, max_j)
    U = generate_empty_2d_array(max_i, max_j)

    # Backtrack key
    bL = generate_empty_2d_array(max_i, max_j)
    bM = generate_empty_2d_array(max_i, max_j)
    bU = generate_empty_2d_array(max_i, max_j)

    # Fill in what we can to initialize
    # M[0][0] is already 0.
    bM[0][0] = GAP_SOURCE

    # First row of lower should be large negative
    # since we simply cannot get to those nodes
    for j in range(0, max_j):
        L[0][j] = -1000
        bL[0][j] = GAP_UNKNOWN
    # Same as first col of upper
    for i in range(0, max_i):
        U[i][0] = -1000
        bU[i][0] = GAP_UNKNOWN


    # Fill in remaining scores.
    for diag in range(1, 2*max(max_i, max_j)):

        # Lower/upper entries first.
        for j in range(diag+1):
            i = diag - j

            # Lower
            if 0 <= j < max_j and 0 < i < max_i:
                vals = [L[i-1][j] - gapextend, M[i-1][j] - gapopen]
                max_val = max(vals)
                max_index = vals.index(max_val)

                L[i][j] = max_val
                if max_index == 0:
                    bL[i][j] = GAP_V_EXTEND
                else:
                    bL[i][j] = GAP_V_OPEN

            # Upper
            if 0 < j < max_j and 0 <= i < max_i:
                vals = [U[i][j-1] - gapextend, M[i][j-1] - gapopen]
                max_val = max(vals)
                max_index = vals.index(max_val)

                U[i][j] = max_val
                if max_index == 0:
                    bU[i][j] = GAP_W_EXTEND
                else:
                    bU[i][j] = GAP_W_OPEN

        # Using L and U, generate the diag entries of M
        for j in range(diag+1):
            i = diag - j

            if not (0 <= j < max_j and 0 <= i < max_i):
                continue

            if i == 0 or j == 0:
                match_score = None
            else:
                match_score = M[i-1][j-1] + score_matrix[v[i-1], w[j-1]]

            vals = [L[i][j], U[i][j], match_score]
            max_val = max(vals)
            max_index = vals.index(max_val)

            M[i][j] = max_val
            if max_index == 0:
                bM[i][j] = GAP_V_CLOSE
            elif max_index == 1:
                bM[i][j] = GAP_W_CLOSE
            else:
                bM[i][j] = GAP_DIAG

    return (L, M, U), (bL, bM, bU)

def LCSBacktrackFit(v, w):

    s = generate_empty_2d_array(len(v)+1, len(w)+1)
    b = generate_empty_2d_array(len(v)+1, len(w)+1)

    # There is a connection between the source and every
    # v node with weight zero.  This means that the
    # left column is all zeros.

    # Fill in the top row and left column
    for i in range(1, len(v)+1):
        s[i][0] = 0
        b[i][0] = SOURCE
    for j in range(1, len(w)+1):
        s[0][j] = s[0][j-1] - 1
        b[0][j] = RIGHT

    # Fill in remaining scores
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):

            # Determine if the highest score is from
            # indel or diagonal
            diag_score = 1
            if v[i-1] != w[j-1]:
                diag_score = -1
            inpath_scores = [s[i-1][j] - 1,
                             s[i][j-1] - 1,
                             s[i-1][j-1] + diag_score]

            max_val = max(inpath_scores)
            max_index = inpath_scores.index(max_val)

            s[i][j] = max_val

            if max_index == 0:
                b[i][j] = DOWN
            elif max_index == 1:
                b[i][j] = RIGHT
            else:
                b[i][j] = DIAG

            # print "({}, {}) [{}, {}] {} {}: {} ({}, {}) = {}".format(i, j,
            #                                                   v[i-1], w[j-1],
            #                                                   words[b[i][j]],
            #                                                   s[i][j], str(inpath_scores),
            #                                                   i-1, j-1, s[i-1][j-1])


    local_max = 0
    for i in range(1, len(v)+1):
        if s[i][len(w)] > local_max:
            local_max = s[i][len(w)]
            local_ij = (i, len(w))

    # Override the last position to link to the max score in the last column
    if local_max > s[len(v)][len(w)]:
        s[len(v)][len(w)] = local_max
        b[len(v)][len(w)] = local_ij

    return s, b


def write_backtracked_alignment(b, v, w):
    aligned_v = ''
    aligned_w = ''

    current_row = len(v)
    current_col = len(w)

    while True:
        if type(b[current_row][current_col]) is tuple:
            #print b[current_row][current_col]
            # Jump to the local alignment starting point.
            temp_row = b[current_row][current_col][0]
            temp_col = b[current_row][current_col][1]
            current_row = temp_row
            current_col = temp_col
        elif b[current_row][current_col] == DIAG:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = w[current_col-1] + aligned_w
            current_row -= 1
            current_col -= 1
        elif b[current_row][current_col] == DOWN:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = '-' + aligned_w
            current_row -= 1
        elif b[current_row][current_col] == RIGHT:
            aligned_v = '-' + aligned_v
            aligned_w = w[current_col-1] + aligned_w
            current_col -= 1
        else:  # SOURCE
            current_row = 0
            current_col = 0

        if current_row == 0 and current_col == 0:
            break

    print aligned_v
    print aligned_w

def write_backtracked_gapopen(backtracks, v, w):

    aligned_v = ''
    aligned_w = ''

    current_layer = 1
    current_row = len(v)
    current_col = len(w)

    while True:
        backtrack_dir = backtracks[current_layer][current_row][current_col]

        if backtrack_dir == GAP_V_CLOSE:
            # Nothing added to strings,
            # move to lower level
            current_layer = 0
        elif backtrack_dir == GAP_W_CLOSE:
            # move to upper level
            current_layer = 2
        elif backtrack_dir == GAP_V_OPEN:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = '-' + aligned_w
            current_layer = 1
            current_row -= 1
        elif backtrack_dir == GAP_W_OPEN:
            aligned_v = '-' + aligned_v
            aligned_w = w[current_col-1] + aligned_w
            current_layer = 1
            current_col -= 1
        elif backtrack_dir == GAP_DIAG:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = w[current_col-1] + aligned_w
            current_col -= 1
            current_row -= 1
        elif backtrack_dir == GAP_V_EXTEND:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = '-' + aligned_w
            current_row -= 1
        elif backtrack_dir == GAP_W_EXTEND:
            aligned_w = w[current_col-1] + aligned_w
            aligned_v = '-' + aligned_v
            current_col -= 1
        else:
            break

    print aligned_v
    print aligned_w




# GAP_V_OPEN = 1
# GAP_V_EXTEND = 2
# GAP_V_CLOSE = 3
# GAP_W_OPEN = 4
# GAP_W_EXTEND = 5
# GAP_W_CLOSE = 6
# GAP_DIAG = 7
# GAP_SOURCE = 8


def write_backtracked_overlap_alignment(b, v, w):
    aligned_v = ''
    aligned_w = ''

    current_row = len(v)
    current_col = len(w)

    while True:
        if type(b[current_row][current_col]) is tuple:
            #print b[current_row][current_col]
            # Jump to the local alignment starting point.
            temp_row = b[current_row][current_col][0]
            temp_col = b[current_row][current_col][1]
            current_row = temp_row
            current_col = temp_col
        elif b[current_row][current_col] == DIAG:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = w[current_col-1] + aligned_w
            current_row -= 1
            current_col -= 1
        elif b[current_row][current_col] == DOWN:
            aligned_v = v[current_row-1] + aligned_v
            aligned_w = '-' + aligned_w
            current_row -= 1
        elif b[current_row][current_col] == RIGHT:
            aligned_v = '-' + aligned_v
            aligned_w = w[current_col-1] + aligned_w
            current_col -= 1
        else:  # SOURCE
            current_row = 0
            current_col = 0

        if current_row == 0 and current_col == 0:
            break

    print aligned_v
    print aligned_w


def OutputLCS(backtrack, v, i, j):

    if i == 0 or j == 0:
        return
    if backtrack[i][j] == DOWN:
        OutputLCS(backtrack, v, i-1, j)
    elif backtrack[i][j] == RIGHT:
        OutputLCS(backtrack, v, i, j-1)
    else:
        OutputLCS(backtrack, v, i-1, j-1)
        sys.stdout.write(v[i-1])


class Node(object):
    def __init__(self, name):
        self.name = name
        self.in_edges = []
        self.out_edges = []
        self.path_score = None
        self.path_predecessors = []

    def add_out_edge(self, name, weight):
        self.out_edges.append([name, weight])

    def add_in_edge(self, name):
        self.in_edges.append(name)


class Graph(object):
    def __init__(self, edge_list):
        self.nodes = {}
        for edge in edge_list:
            start_node = edge[0]
            end_node = edge[1]
            edge_weight = edge[2]
            if start_node not in self.nodes:
                self.nodes[start_node] = Node(start_node)
            self.nodes[start_node].add_out_edge(end_node, edge_weight)
            if end_node not in self.nodes:
                self.nodes[end_node] = Node(end_node)
            self.nodes[end_node].add_in_edge(start_node)


    def calculate_path_information(self, source_node):

        # Prune stems other than the source
        while True:
            purge_list = []
            for node_name, node in self.nodes.items():
                if node_name == source_node:
                    continue
                if len(node.in_edges) > 0:
                    continue

                if len(node.out_edges) > 0:
                    # Remove the node.
                    purge_list.append(node_name)
                    for downstream_node_name in node.out_edges:
                        self.nodes[downstream_node_name[0]].in_edges.remove(node_name)

            if not purge_list:
                break

            for purge_node in purge_list:
                # print "purging {}".format(purge_node)
                del self.nodes[purge_node]

        # NONE scores mean that a node has not been visited.
        # Set the source node to have a score of 0
        self.nodes[source_node].path_score = 0

        while True:
            changed_node = False
            # Loop over all nodes in the graph
            for node_str in self.nodes:

                node = self.nodes[node_str]

                if node.path_score is not None:
                    continue

                inputs_complete = True
                for in_edge in node.in_edges:
                    if self.nodes[in_edge].path_score is None:
                        inputs_complete = False
                        break
                if inputs_complete is False:
                    continue

                # We have a complete set of input path scores, so calculate this node's path score
                changed_node = True
                node.path_score = -1000
                for in_edge in node.in_edges:
                    parent_edge = [b for b in self.nodes[in_edge].out_edges if b[0] == node.name]
                    this_path_score = self.nodes[in_edge].path_score + parent_edge[0][1]
                    if this_path_score > node.path_score:
                        node.path_score = this_path_score
                        node.path_predecessors = [in_edge]
                    elif this_path_score == node.path_score:
                        node.path_predecessors.append(in_edge)

            if changed_node is False:
                break

    def backtrack_longest_path(self, source_node, sink_node):
        # First, print the score
        print int(self.nodes[sink_node].path_score)

        # Assemble the path backwards
        mypath = [sink_node]

        while mypath[-1] != source_node:
            prev_edge = self.nodes[mypath[-1]].path_predecessors[0]
            mypath.append(prev_edge)

        mypath.reverse()

        #print "->".join(mypath)
        return mypath

