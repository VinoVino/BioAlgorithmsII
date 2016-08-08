__author__ = 'jcovino'
from sys import  argv


"""
CODE CHALLENGE: Solve the Probability of an Outcome Given a Hidden Path Problem.
     Input: A string x, followed by the alphabet from which x was constructed, followed by
     a hidden path pie, followed by the states States and emission matrix Emission of an HMM

Extra Dataset

zzzyxyyzzx
--------
x y z
--------
BAAAAAAAAA
--------
A B
--------
	x	y	z
A	0.176	0.596	0.228
B	0.225	0.572	0.203
Sample Output:
3.59748954746e-06


problem

	x	y	z
A	0.546	0.037	0.417
B	0.401	0.277	0.322



"""





def main(argv):

    Distances=[]
    with open(argv[1], "r") as fstream:
       Path1=fstream.readline().rstrip()
       Path2=fstream.readline().rstrip()
       print Path1
       print Path2

    Score = {'Ax': 0.546, 'Ay': 0.037, 'Az':0.417,
             'Bx':0.401,   'By':0.277, 'Bz': 0.322
             }

    #break up path into steps
    steps=[]
    for i in range(len(Path1)):
          step=Path2[i]+Path1[i]
          steps.append(step)

    totalscore=1

    print steps
    for step in steps:
        stepScore= Score[step]
        print step,  stepScore
        totalscore=totalscore*stepScore


    print totalscore









if __name__== "__main__":
    main(argv)
