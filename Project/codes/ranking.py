import pandas as pd
import numpy as np

df1 = pd.read_csv("Result-Most-Runs-2020.csv")
df2 = pd.read_csv("Result-Most-Wickets-2020.csv")

## scores for starting order batsman
batrank = (df1.iloc[:,5]/df1.iloc[:,2])/30  +  (df1.iloc[:,9]/100)
a = np.zeros((len(batrank),))
a[df1.iloc[:,3]>10] = 1
batrank = batrank*a
batrankMap = {}
for i in range(len(batrank)):
    batrankMap[df1.iloc[i,1]] = batrank[i]

## scores for middle order batsman
midrank =  (df1.iloc[:,9]/100) + (df1.iloc[:,13]/max(df1.iloc[:,13]))
midrankMap = {}
for i in range(len(midrank)):
    midrankMap[df1.iloc[i,1]] = midrank[i]

## scores for bowlers
ballrank = (df2.iloc[:,6]/max(df2.iloc[:,6])) + (7/df2.iloc[:,9])
ballrankMap = {}
for i in range(len(ballrank)):
    ballrankMap[df2.iloc[i,1]] = ballrank[i]

opener = {k: v for k, v in sorted(batrankMap.items(), key=lambda item: item[1])}
middle = {k: v for k, v in sorted(midrankMap.items(), key=lambda item: item[1])}
bowler = {k: v for k, v in sorted(ballrankMap.items(), key=lambda item: item[1])}

olist = []   # ranks of opening batsman
mlist = []   # rabks of middle batsmen
blist = []   # ranks of bowlers
for i in opener :
    olist.append([i,opener[i]])
olist.reverse()
for i in middle :
    mlist.append([i,middle[i]])
mlist.reverse()
for i in bowler :
    blist.append([i,bowler[i]])
blist.reverse()


blist