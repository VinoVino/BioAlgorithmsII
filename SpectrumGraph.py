__author__ = 'jcovino'
from sys import  argv
import sys

"""
CODE CHALLENGE: Construct the graph of a spectrum.
     Given: A space-delimited list of integers Spectrum.
     Return: Graph(Spectrum).

Note: Throughout this chapter, all dataset problems implicitly use the standard integer-valued mass table for the regular twenty amino acids.
Examples sometimes use the toy amino acid alphabet X, Y whose masses are 4 and 5, respectively.

Sample Input:
57 71 154 185 301 332 415 429 486
Sample Output:
0->57:G
0->71:A
57->154:P
57->185:K
71->185:N
154->301:F
185->332:F
301->415:N
301->429:K
332->429:P
415->486:A
429->486:G

"""

def constructGraph(massarray,AAmasstable):
    print
    for i in range (len(massarray)):
        for j in range (len(massarray)):
            masssubtract=int(massarray[i]-massarray[j])
            if masssubtract in AAmasstable:
                startstop=[]
                startstop.append(massarray[j])
                startstop.append(massarray[i])
                #print masssubtract, startstop
                stringStartstop=str(startstop[0])+"->"+str(startstop[1])
                sys.stdout.write(stringStartstop)
                sys.stdout.write(":")
                sys.stdout.write(AAmasstable[masssubtract])
                sys.stdout.write("\n")
                #stringStartstop, ":",AAmasstable[masssubtract]





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

    print AAmasstable
    print massarray

    constructGraph(massarray,AAmasstable)




if __name__== "__main__":
    main(argv)
