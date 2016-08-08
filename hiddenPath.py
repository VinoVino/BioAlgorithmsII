__author__ = 'jcovino'
from sys import  argv


"""
Given: A hidden path pie followed by the states States and transition matrix Transition of an HMM

Extra Dataset

Sample Input:
ABABBBAAAA
--------
A B
--------
	A	B
A	0.377	0.623
B	0.26	0.74
Sample Output:
0.000384928691755
"""





def main(argv):

    Distances=[]
    with open(argv[1], "r") as fstream:
       Path=fstream.readline().rstrip()
       print Path

    Score = {'AA': 0.655, 'AB': 0.345, 'BA':0.46, 'BB':0.54}

    #break up path into steps
    steps=[]
    for i in range(len(Path)-1):
        step=Path[i:i+2]
        steps.append(step)
    totalscore=0.5


    for step in steps:
        stepScore= Score[step]
        totalscore=totalscore*stepScore


    print totalscore









if __name__== "__main__":
    main(argv)
