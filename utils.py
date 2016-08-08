#!/usr/bin/env python
__author__ = 'erikreckase'

from itertools import combinations, permutations
from collections import defaultdict
from math import exp, sqrt, log10


def pdist(p1, p2):

    return sqrt(sum(pow(p1[i]-p2[i], 2) for i in range(len(p1))))


def MaxDistance(data, centers):

    maxdist = 0.0
    maxpt = None
    for point in data:
        mindistfromcenters = min([pdist(point, centers[i]) for i in range(len(centers))])
        if mindistfromcenters > maxdist:
            maxdist = mindistfromcenters
            maxpt = point

    return maxpt, maxdist


def FarthestFirstTraversal(data, k):

    # choose the first element of data to be the first center
    center = [data[0]]

    # Loop until we have k centers
    while len(center) < k:

        # The next center is the point in data that is
        # furthest from the nearest center.
        center.append(MaxDistance(data, center))

    return center

def SquaredErrorDistortion(data, centers):

    # Loop over the points in the data
    total_distortion = 0
    for point in data:
        mindistfromcenters = min([pdist(point, centers[i]) for i in range(len(centers))])
        total_distortion += mindistfromcenters

    total_distortion /= float(len(data))

    return total_distortion


def LloydAlgorithm(data, centers):

    center_groups = defaultdict(list)

    for point in data:
        dists = [pdist(point, centers[i]) for i in range(len(centers))]
        min_dist = min(dists)
        min_center = dists.index(min_dist)

        center_groups[min_center].append(point)

    new_centers = list()
    for i in range(len(centers)):
        avg_points = center_groups[i]
        new_center = [0] * len(data[0])
        for coord in range(len(data[0])):
            new_center[coord] = float(sum(avg_point[coord] for avg_point in avg_points))/float(len(avg_points))
        new_centers.append(new_center)

    return new_centers

def expfunc(stiffness, dist):

    return exp(-1 * stiffness * dist)


def HiddenMatrix(data, centers, stiffness=0):

    num_pts = len(data)
    num_centers = len(centers)

    hidden = list()
    for _ in range(num_centers):
        hidden.append([0] * num_pts)

    for pti in range(num_pts):

        # Get the distance between this point and the centers.
        center_dists = [pdist(data[pti], centers[ci]) for ci in range(num_centers)]
        # Get the weighted values
        if stiffness == 0:
            partition_values = [1.0/(dist*dist) for dist in center_dists]
        else:
            partition_values = [expfunc(stiffness, dist) for dist in center_dists]

        sum_partition = sum(partition_values)

        if sum_partition == 0.0:
            print center_dists

        for ci in range(num_centers):
            if sum_partition != 0.0:
                hidden[ci][pti] = partition_values[ci]/sum_partition
            else:
                hidden[ci][pti] = 0.0


    return hidden


def ExpectMax(data, centers, stiffness):

    # Performs one E step and one M step
    num_pts = len(data)
    num_centers = len(centers)

    # E step - generate hidden matrix for this set of centers
    hidden = HiddenMatrix(data, centers, stiffness)

    # for ci in range(num_centers):
    #     print "H{}".format(ci), hidden[ci]

    # M step - perform a weighted average of the clustered points
    # scaled by the values of the hidden matrix.
    new_centers = list()
    for ci in range(num_centers):
        hm_row = hidden[ci]

        sum_hm_row = sum(hm_row)

        new_coords = []

        for coord in range(len(data[0])):
            # We must take the dot product of each coord and the hidden values
            coord_numerator = sum([hm_row[i] * data[i][coord] for i in range(num_pts)])
            new_coords.append(coord_numerator / sum_hm_row)

        new_centers.append(new_coords)

    return new_centers


def ExpectMaxIter(data, centers, stiffness, iters):

    for _ in range(iters):
        new_centers = ExpectMax(data, centers, stiffness)
        centers = new_centers

    for center in centers:
        print " ".join("{:.3f}".format(coord) for coord in center)


def dashdelim(lines):
    sections = []
    section = []
    for line in lines:
        if line.startswith('------'):
            sections.append(section)
            section = []
        else:
            section.append(line)

    sections.append(section)
    return sections

def parsematrix(lines):
    ykeys = lines[0].strip().split('\t')
    mat = defaultdict(dict)
    for line in lines[1:]:
        fields = line.strip().split('\t')
        xkey = fields[0]
        for i in range(len(ykeys)):
            mat[xkey][ykeys[i]] = float(fields[i+1])

    return mat


def get_seed_cols(alignments, theta):

    seed_cols = []
    num_alignments = len(alignments)
    for i in range(len(alignments[0])):
        poss_states = [alignment[i] for alignment in alignments]
        num_spaces = poss_states.count('-')
        frac = float(num_spaces)/float(num_alignments)
        if frac < theta:
            seed_cols.append(i)

    return seed_cols


def prob_hidden_path(path, trans_mat):

    # Start with 0.5 for the first state
    p = 0.5

    for i in range(len(path)-1):
        state_from = path[i]
        state_to = path[i+1]
        p *= trans_mat[state_from][state_to]

    return p

def prob_outcome(out_seq, state_path, emiss_mat):

    # For letter in the out seq, scale by
    # the probability that the state emitted this letter
    p = 1.0

    for i in range(len(out_seq)):
        p *= emiss_mat[state_path[i]][out_seq[i]]

    return p


def outcome_likelihood(sequence, states, trans_mat, emiss_mat):

    forward = dict()
    for init_state in states:
        forward[init_state] = [(emiss_mat[init_state][sequence[0]]/float(len(states)))]

    print forward

    for si in range(1, len(sequence)):
        for end_state in states:
            # next forward value is
            # sum ( forward[state] * trans_mat[state][end_state] * emiss_mat[end_state][sequence[si]] )
            # over all states
            next_fwd = 0.0
            for start_state in states:
                next_fwd += forward[start_state][si-1] * \
                    (trans_mat[start_state][end_state] * emiss_mat[end_state][sequence[si]])
            forward[end_state].append(next_fwd)
        print forward

    totalp = sum([forward[state][-1] for state in states])

    print "{:.16e}".format(totalp)


def get_hmm_states(num_seeds):
    hmm_states = ['S', 'I0']
    for i in range(num_seeds):
        hmm_state_num = i+1
        hmm_states.extend('M{0} D{0} I{0}'.format(hmm_state_num).split())
    hmm_states.append('E')
    return hmm_states

def norm_matrix(matrix):
    for major_key in matrix:
        norm = sum(list(matrix[major_key].itervalues()))
        if norm > 0:
            for minor_key in matrix[major_key]:
                matrix[major_key][minor_key] = float(matrix[major_key][minor_key]) / float(norm)

def pseudo_transition_matrix(matrix, states, sig):
    for major_key in matrix:
        if major_key == 'E':
            continue
        hmm_idx = 0
        if major_key != 'S':
            hmm_idx = int(major_key[1:])

        matrix[major_key]['I{}'.format(hmm_idx)] += sig
        matchstr = 'M{}'.format(hmm_idx+1)
        if matchstr in states:
            matrix[major_key]['M{}'.format(hmm_idx+1)] += sig
        else:
            # We must be at the last I state
            matrix[major_key]['E'] += sig
        delstr = 'D{}'.format(hmm_idx+1)
        if delstr in states:
            matrix[major_key]['D{}'.format(hmm_idx+1)] += sig

        norm = sum(list(matrix[major_key].itervalues()))
        if norm > 0:
            for minor_key in matrix[major_key]:
                matrix[major_key][minor_key] = float(matrix[major_key][minor_key]) / float(norm)

def pseudo_emission_matrix(matrix, states, letters, sig):
    for major_key in states:
        if major_key.startswith('M') or major_key.startswith('I'):
            for letter in letters:
                matrix[major_key][letter] += sig
        else:
            continue

        norm = sum(list(matrix[major_key].itervalues()))
        if norm > 0:
            for minor_key in matrix[major_key]:
                matrix[major_key][minor_key] = float(matrix[major_key][minor_key]) / float(norm)



def print_matrix(matrix, left_labels, top_labels):

    # Print header
    print "\t" + "\t".join(top_labels)

    # Print rows
    for ll in left_labels:
        print ll + "\t" + "\t".join(["{:5.3f}".format(matrix[ll][tl]) for tl in top_labels])


def profile_hmm(theta, all_states, alignments, pseudo_sig=0.0):

    al_len = len(alignments[0])

    # Get the list of seed positions
    seeds = get_seed_cols(alignments, theta)

    # Create the list of states
    hmm_states = get_hmm_states(len(seeds))

    state_counts = {hmm_state: defaultdict(int) for hmm_state in hmm_states}
    base_counts = {hmm_state: defaultdict(int) for hmm_state in hmm_states}

    # Loop over alignments
    for alignment in alignments:
        cur_state = 'S'
        hmm_snum = 0
        for a_pos in range(al_len):
            is_seed = a_pos in seeds
            align_char = alignment[a_pos]

            # First check for insertion.
            # Probably more complicated than is necessary
            if not is_seed:
                if align_char is not '-':
                    next_state = 'I{}'.format(hmm_snum)
                    base_counts[next_state][align_char] += 1
                else:
                    continue
            else:
                # increment the state num
                hmm_snum += 1

                # Check for match/deletion
                if align_char is '-':
                    # This is a deletion
                    next_state = 'D{}'.format(hmm_snum)
                else:
                    # Match
                    next_state = 'M{}'.format(hmm_snum)
                    base_counts[next_state][align_char] += 1

            state_counts[cur_state][next_state] += 1
            cur_state = next_state

        # Add the final state to E
        state_counts[cur_state]['E'] += 1

    # What we have in the crazydicts is the raw counts, we have to normalize
    norm_matrix(state_counts)
    norm_matrix(base_counts)

    if pseudo_sig > 0:
        pseudo_transition_matrix(state_counts, hmm_states, pseudo_sig)
        pseudo_emission_matrix(base_counts, hmm_states, all_states, pseudo_sig)

    return state_counts, base_counts, hmm_states


def param_est(emit_str, emit_alpha, state_str, state_alpha):

    # Store counts of state transitions and emitted values
    state_change = dict()
    emitted = dict()
    for letter in state_alpha:
        state_change[letter] = defaultdict(int)
        emitted[letter] = defaultdict(int)

    for i in range(len(emit_str)):
        emitted[state_str[i]][emit_str[i]] += 1

    for i in range(len(state_str)-1):
        state_change[state_str[i]][state_str[i+1]] += 1

    # Check for never getting into a state
    for state in state_alpha:
        if len(state_change[state].keys()) == 0:
            # All next states are equal prob
            for s in state_alpha:
                state_change[state][s] = 1
            # It also follows that emission probs for this state are also not defined
            for em in emit_alpha:
                emitted[state][em] = 1

    norm_matrix(emitted)
    norm_matrix(state_change)

    return emitted, state_change


def viterbi_edges(output_str, emiss_matrix, trans_matrix, trans_alpha):

    edges = []
    for i in range(len(output_str)):
        emitted = output_str[i]
        statenumstr = str(i+1)
        if i == 0:
            # Set up source
            # Weights are simply the probability that each
            # state emits the emitted signal
            # Use logs so we can keep the scoring the same in DAG
            for state in trans_alpha:
                node_name = state + statenumstr
                p = emiss_matrix[state][emitted]
                if p > 0:
                    edges.append(['source', node_name, log10(p)])
            continue

        # We have to establish an edge from each state to each state
        for start_state in trans_alpha:
            start_node = start_state + str(i)
            for end_state in trans_alpha:
                end_node = end_state + statenumstr
                p = trans_matrix[start_state][end_state] * emiss_matrix[end_state][emitted]
                if p > 0:
                    edges.append([start_node, end_node, log10(p)])
    # We need a sink
    for state in trans_alpha:
        # The last statenumstr is the start node
        edges.append([state + statenumstr, 'sink', 0])

    return edges