__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict
from utils_15 import Graph

"""
CODE CHALLENGE: Implement PSMSearch to solve the Peptide Search Problem.
     Given: A set of space-delimited spectral vectors SpectralVectors, an amino acid string
     Proteome, and an integer threshold.
     Return: The set PSMthreshold(Proteome, SpectralVectors).

Extra Dataset

Sample Input:
-1 5 -4 5 3 -1 -4 5 -1 0 0 4 -1 0 1 4 4 4
-4 2 -2 -4 4 -5 -1 4 -1 2 5 -3 -1 3 2 -3
XXXZXZXXZXZXXXZXXZX
5
Sample Output:
XZXZ
"""

def generatekmers(lowLength,highLength,protein):
    peptidekmers=[]

    window=lowLength
    while window < highLength:
        for i in range(len(protein)-window):
            subpeptide=protein[i:i+window]
            peptidekmers.append(subpeptide)
        window=window+1

    return peptidekmers

def scorepeptides(peptidekmers,vectorList,AA_Mass):
    filter_peptidekmers=[]
    for peptide in peptidekmers:
        totalMass=0
        mass=0
        for aa in peptide:
            mass=AA_Mass[aa]
            totalMass=totalMass+mass
        if totalMass == len(vectorList):
            #print totalMass
            filter_peptidekmers.append(peptide)


    maxScore=0
    Toppep=''

    for peptide in filter_peptidekmers:
        score=0
        mass=0
        for aa in peptide:
            mass=AA_Mass[aa] + mass
            #if mass< len(vectorList):
            score=vectorList[mass-1] +score
        if score > maxScore:
            maxScore=score
            Toppep=peptide
        # if score == maxScore:
        #     Toppep.append(peptide)
    return Toppep, maxScore


def main(argv):
    Mass_AA={}
    AA_Mass={}

    with open(argv[1], "r") as massTable:
        for line in massTable:
            line=line.rstrip()
            tokens=line.split(" ")
            AAsymbol=tokens[0]
            mass=int(tokens[1])
            Mass_AA[mass]=AAsymbol
            AA_Mass[AAsymbol]=mass

    with open(argv[2], "r") as VectorInput:
        vector=VectorInput.readlines()
        # add zero to vector input--you do it

    with open(argv[3],"r") as proteinInput:
        protein=(proteinInput.readline().rstrip())

    threshold=143
    Masslist=Mass_AA.keys()

    vector=map(str.strip, vector)

    AnswerList=[]
    for vectorlist in vector:
        vector=vectorlist.split(" ")
        vectorInt=map(int,vector)
        massofPeptide=len(vectorInt)
        highLength= massofPeptide/57
        lowLength= massofPeptide/186
        peptidekmers=generatekmers(lowLength,highLength,protein)
        TopPep, maxScore=scorepeptides(peptidekmers,vectorInt,AA_Mass)
        if maxScore >= threshold:
            AnswerList.append(TopPep)

    setAnswer=set(AnswerList)

    for element in setAnswer:
        print element




if __name__== "__main__":
    main(argv)
