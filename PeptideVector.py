__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict

"""
CODE CHALLENGE: Solve the Converting a Peptide into a Peptide Vector Problem.
     Given: An amino acid string P.
     Return: The peptide vector of P (in the form of space-separated integers).

Extra Dataset

Sample Input:
XZZXX
Sample Output:
0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 1

Time Limit: 5 mins
"""

def Vector(Sequence,AAmasstable):
    print Sequence
    AnswerList=[]

    massTotal=0
    sum=0
    for letter in Sequence:
        mass= AAmasstable[str(letter)]
        massTotal=massTotal+mass

        for i in range (mass):
            sum=sum+1
            if sum==massTotal:
                AnswerList.append(1)
            else:
                AnswerList.append(0)



    for element in AnswerList:
        print element,

def main(argv):
    AAmasstable={}


    with open(argv[1], "r") as massTable:
        for line in massTable:
            line=line.rstrip()
            tokens=line.split(" ")
            AAsymbol=tokens[0]
            mass=int(tokens[1])
            AAmasstable[AAsymbol]=mass

    Sequence=raw_input("Enter sequence: ")

    Vector(Sequence,AAmasstable)






if __name__== "__main__":
    main(argv)
