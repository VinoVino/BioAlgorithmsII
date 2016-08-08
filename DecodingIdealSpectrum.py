__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict

"""
CODE CHALLENGE: Solve the Decoding an Ideal Spectrum Problem.
     Given: A space-delimited list of integers Spectrum.
     Return: An amino acid string that explains Spectrum.

Extra Dataset

Sample Input:
57 71 154 185 301 332 415 429 486
Sample Output:
GPFNA

Time Limit: 5 mins

DecodingIdealSpectrum(Spectrum)
     construct Graph(Spectrum)
     for each path Path from source to sink in Graph(Spectrum)
          Peptide = the amino acid string spelled by the edge labels of Path
          if IdealSpectrum(Peptide) = Spectrum
                return Peptide


"""
def constructGraph(massarray,AAmasstable):
    print
    pathGraph=defaultdict(list)
    for i in range (len(massarray)):
        for j in range (len(massarray)):
            masssubtract=int(massarray[i]-massarray[j])
            if masssubtract in AAmasstable:
                pathGraph[massarray[j]].append(massarray[i])

    
    PathList= find_path(pathGraph,0,massarray[-1])

    print "----> ", PathList
    print
    for i in range (len(PathList)-1):
        Score=PathList[i+1]-PathList[i]
        AA=AAmasstable[Score]
        #print AA,
        sys.stdout.write(str(AA))
    print

def find_path(graph, start, end, path=[]):
        #recursive algorithm-- study this
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None


def main(argv):
    AAmasstable={}


    with open(argv[1], "r") as massTable:
        for line in massTable:
            line=line.rstrip()
            tokens=line.split(" ")
            AAsymbol=tokens[0]
            mass=int(tokens[1])
            AAmasstable[mass]=AAsymbol

    massinput=raw_input("Enter spectrum: ")
    massarray=massinput.split(" ")
    massarray=map(int,massarray)


    constructGraph(massarray,AAmasstable)




if __name__== "__main__":
    main(argv)
