import itertools
import re
import json
from wordlelib import *

# Bring in the top 10k list from the frequency analysis pass in as an optimization
f = open("bests.json","r")
bests = [item[1] for item in json.load(f)]
f.close()

# Import the precomputed colormatrix
f = open("colormatrix.json")
colormatrix = json.load(f)
f.close()

import time
best = len(ANSWERS)**2
possibilities = []
for k in range(0,500):
    pair = bests[k]
    w0 = list(pair[0])
    w1 = list(pair[1])
    count = 0
    #now = time.time()
    for c in range(len(ANSWERS)):
        i = DIC.index(pair[0])
        j = DIC.index(pair[1])
        if colormatrix[i][c] and colormatrix[j][c]:
            ans1 = filter_ans(ANSWERS,colormatrix[i][c][0],colormatrix[i][c][1],colormatrix[i][c][2])
            count += len(filter_ans(ans1,colormatrix[j][c][0],colormatrix[j][c][1],colormatrix[j][c][2]))
    possibilities.append((k,count/len(ANSWERS)))
    if count<best:
        best = count
        best_w = (w0,w1)
        print(best/len(ANSWERS), "".join(w0),"".join(w1))
    #print("Time: ",time.time()-now)

best = ["".join(best_w[0]),"".join(best_w[1])]


possibilities.sort(key=lambda y: y[0])
f = open("poss.csv","w")
for p in possibilities:
    f.write(p[0],",",p[1])
f.close()

# Figure out subsequent words.

# How much is a Yellow/Grey worth relative to Greens?
# 
YELLOW_FACTOR = 3

# We're going to use itertools to automatically generate unique combinations of 3 words from the dictionary
import itertools
# And json to persist data
import json

# Counters for letters at each position (for green squares)
let0 = {}
let1 = {}
let2 = {}
let3 = {}
let4 = {}
# Counter for letters in any position (for yellow squares)
yellows = {}

import string
letters=list(string.ascii_lowercase)

# Initialize our counters
for l in letters:
    let0[l] = 0
    let1[l] = 0
    let2[l] = 0
    let3[l] = 0
    let4[l] = 0
    yellows[l] = 0

# Count up the letters for each answer
for answer in ANSWERS:
    let0[answer[0]] += 1
    let1[answer[1]] += 1
    let2[answer[2]] += 1
    let3[answer[3]] += 1
    let4[answer[4]] += 1
    yellows[answer[0]] += 1
    yellows[answer[1]] += 1
    yellows[answer[2]] += 1
    yellows[answer[3]] += 1
    yellows[answer[4]] += 1

# For ease of code, convert letter counters to frequencies
freq0 = {}
freq1 = {}
freq2 = {}
freq3 = {}
freq4 = {}
freqG = [freq0,freq1,freq2,freq3,freq4]
freqY = {}

for l in let0:
    freq0[l] = let0[l] / len(ANSWERS)
for l in let1:
    freq1[l] = let1[l] / len(ANSWERS)
for l in let2:
    freq2[l] = let2[l] / len(ANSWERS)
for l in let3:
    freq3[l] = let3[l] / len(ANSWERS)
for l in let4:
    freq4[l] = let4[l] / len(ANSWERS)
for l in yellows:
    freqY[l] = yellows[l] / (len(ANSWERS)*5)

# The logic for determining the value of a guess
# 'givens' is the list of prior guesses
def value(word, freqG, freqY, yFactor=YELLOW_FACTOR, givens=[]):
    # Count up the number of greens expected
    greens = 0.0
    for i in range(5):
        # Don't double count letters already guessed
        g = ""
        for given in givens:
            g += given[i]
        if word[i] not in g:
            greens+=freqG[i][word[i]]
    # Count up yellows expected
    yellows = 0.0
    # Count only unique letters...
    for l in ''.join(set(word)):
        # ... not already guessed
        if l not in ''.join(givens):
            yellows += freqY[l]
    # Multiply by the Yellow Factor
    return greens + yellows*yFactor

# Now let's figure out what the next guesses should be, in case we keep striking out
# We might also want to bump up the Yellow Factor since we're getting more and more desperate for yellows as we run out of guesses 
bestfreq = 0.0
best.append("")
for i in range(1,5):
    for word in DIC:
        # Pass in the best words list as givens
        f = value(word,freqG,freqY,YELLOW_FACTOR+i, best[0:-1])
        if f > bestfreq:
            bestfreq = f
            best[-1] = word
    print(bestfreq,best[-1])
    bestfreq = 0.0
    best.append("")

print("Best guesses: ",best[0:-1])
# This code should result in: ['toile', 'saury', 'dench', 'biped', 'femal', 'wroot']