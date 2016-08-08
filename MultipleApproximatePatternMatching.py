__author__ = 'jcovino'
from sys import argv
import itertools
from collections import defaultdict
"""
You should now be ready to design your own approach to solve the Multiple Approximate Pattern Matching Problem and use this solution to map real sequencing reads.

CODE CHALLENGE: Solve the Multiple Approximate Pattern Matching Problem.
     Input: A string Text, followed by a collection of strings Patterns, and an integer d.
     Output: All positions where one of the strings in Patterns appears as a substring of Text with
     at most d mismatches.

Extra Dataset

Sample Input:
ACATGCTACTTT
ATT GCC GCTA TATT
1
Sample Output:
2 4 4 6 7 8 9
"""


def mismatch(word, num_mismatches, letters='ACGT'):
    """ Provides an iterator over all words exactly num_mismatches away
        from the original word.
    http://stackoverflow.com/questions/11679855/introducing-mutations-in-a-dna-string-in-python
    :param word: input word to vary
    :type word: str
    :param num_mismatches: number of different mismatches in each result word
    :type num_mismatches: int
    :param letters: letters in the alphabet ('ACGT' would be appropriate here)
    :type letters: str
    :return: iterator, returns words with appropriate mismatches
    """

    # Loop over all combinations of locations to create a mismatch
    for locs in itertools.combinations(range(len(word)), num_mismatches):
        # Create a list of single-char lists for use in product call below
        this_word = [[char] for char in word]
        # Loop over each location and make the substitution list
        for loc in locs:
            orig_char = word[loc]
            # Replace the single char with the new options for that char in a list
            this_word[loc] = [l for l in letters if l != orig_char]
        # Calling product generates all combinations of the list elements,
        # which is pretty darn neat.
        for poss in itertools.product(*this_word):
            #print ''.join(poss)
            yield ''.join(poss)

def all_mismatches(word, max_mismatches, letters='ACGT'):
    """ Loop over max mismatches and provide mismatch results.
    :param word: input sequence to vary
    :param max_mismatches: max number of mismatches permitted
    :param letters:
    :return:
    """
    for m in range(max_mismatches+1):
        for poss in mismatch(word, m, letters):
            yield poss


def findKmerPositions(parent,kmers):
    kmerLength=len(kmers[0])
    #print parent
    #print kmerLength
    parent_kmers=defaultdict(list)

    # fill default dict list- kmers and starting position of kmers from Parent string
    i=0
    while i < len (parent)-kmerLength+1:
        tempkmer= parent[i:i+kmerLength]
        #print tempkmer
        parent_kmers[tempkmer].append(i)
        i=i+1
    #print parent_kmers

    positions_kmers=[]
    # identify if kmers are in pattern and record starting position using dictionary
    for kmer in kmers:
        if kmer in parent_kmers:
            positions_kmers.append(parent_kmers[kmer])

    #print positions_kmers
    answer=[]
    for element in positions_kmers:
        for item in element:
            answer.append(item)

    answer.sort()
    #print answer


    return answer


def main(argv):
    PatternInput=[]
    with open(argv[1],"r") as fstream:
            lineInput = fstream.readline()
            PatternInput=fstream.readline()
            Mismatches=int(fstream.readline())

    lineInput=lineInput.rstrip()
    PatternInput=PatternInput.rstrip()

    split_PatternInput=PatternInput.split(" ")

    MismatchKmers=[]
    for pattern in split_PatternInput:   # generate all mismatches for each pattern
      mismatches=list(all_mismatches(pattern,Mismatches,letters='ACGT'))
      MismatchKmers.append(mismatches)



    MatchSpots=[]
    for MisMatchKmerList in MismatchKmers:   # find all matches to each mismatch list for each pattern
        MatchSpots.append(findKmerPositions(lineInput,MisMatchKmerList))


    finaAnswerList=[]
    for topLists in MatchSpots:
        for innerList in topLists:
            finaAnswerList.append(innerList)
    Sorted_FinalAnswerList=sorted(finaAnswerList)

    for item in Sorted_FinalAnswerList:
        print item,  # print without comma and not in list as this is required



if __name__== "__main__":
    main(argv)