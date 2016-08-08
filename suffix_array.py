__author__ = 'jcovino'
from sys import argv
from random import randint
"""
Suffix Array Construction Problem: Construct the suffix array of a string.
     Input: A string Text.
     Output: SuffixArray(Text).

CODE CHALLENGE: Solve the Suffix Array Construction Problem.

Sample Input:
     AACGATAGCGGTAGA$

Sample Output:
     15, 14, 0, 1, 12, 6, 4, 2, 8, 13, 3, 7, 9, 10, 11, 5
"""
def suffixArray (substringList, subStringDict):
    #print substringList
    substringList.sort()
    #print substringList
    answer=[]
    for item in substringList:
        answer.append(subStringDict[item])

    return answer

def main(argv):

    with open(argv[1],"r") as fstream:
        for line in fstream:
            lineInput = line.rstrip()

    substringList=[]
    substringDict={}
    for index in range  (0,len(lineInput)):
        substring= lineInput[index:]
        substringList.append(substring)
        substringDict[substring]=index

    Answer=suffixArray(substringList,substringDict)



    fileOut=open('Answer.txt','w')

    for item in Answer:
       fileOut.write(str(item))
       fileOut.write(', ')


    fileOut.close()



if __name__== "__main__":
    main(argv)