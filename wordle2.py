import re
import json
from os.path import exists
from wordlelib import *
import time

colormatrix = []
if not exists("colormatrix.json"):
    print("Color matrix pre-compute not found; regenerating...")
    exit()
    for word in DIC:
        w = list(word)
        row = []
        #now = time.time()
        for ans in ANSWERS:
            if word == ans:
                row.append(None)
            a = list(ans)
            greens, yellows, grays = color(a,w)
            # print("**********")
            # print(word)
            # print(ans)
            # print(greens)
            # print(yellows)
            # print(grays)
            row.append((greens,yellows,list(grays)))
        colormatrix.append(row)
        #print("Time: ",time.time()-now)

    f = open("colormatrix.json","w")
    json.dump(colormatrix,f)
    f.close()
else:
    f = open("colormatrix.json")
    colormatrix = json.load(f)
    f.close()


best = len(ANSWERS)**2
best_w0 = ""
best_w1 = ""
now = time.time()
f = open("best_avg.json","w")
for i in range(len(DIC[:1300])):
    for j in range(len(DIC[i:1300])):
        #print(colormatrix[i][j])
        # print("*******")
        # print(DIC[i])
        # print(DIC[j])
        # print(colormatrix[i][j])
        # print(filter_ans(ANSWERS,colormatrix[i][j][0],colormatrix[i][j][1],colormatrix[i][j][2]))
        count = 0
        for c in range(len(ANSWERS)):
            if colormatrix[i][c] and colormatrix[j][c]:
                ans1 = filter_ans(ANSWERS,colormatrix[i][c][0],colormatrix[i][c][1],colormatrix[i][c][2])
                count += len(filter_ans(ans1,colormatrix[j][c][0],colormatrix[j][c][1],colormatrix[j][c][2]))
        if count < best:
            best = count
            best_w0 = DIC[i]
            best_w1 = DIC[j]
            print(best/len(ANSWERS), best_w0, best_w1)
print("Time: ",time.time()-now)
print(best/len(ANSWERS), best_w0, best_w1)