import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def total(df,ch):
    ans=0
    for i in df.index:
        ans+= df[ch][i]
    return ans

def moving_avg(a):
    avg = sum(a)/len(a)
    s=[a[0]]; phi=0.4; epsi=0
    for i in range(len(a)-1):
        epsi = s[-1]-a[i]
        s.append(avg + phi*(epsi))
    return s

def plot_values(a):
    ans=[]
    for x in range(0,12):
        s=0
        for j in range(len(a)):
            s = s + a[j]*(x**j)
        ans.append(s)
    return ans



s='Result-Most-Fours-'
tot_team = [8,8,8,10,9,9,8,8,8,8,8,8]
tot_each_season4 = []; avg_each_season4 = []
for i in range(2008,2020):
    df=pd.read_csv(s+str(i)+'.csv')
    tot = total(df,'4s')
    tot_each_season4.append(tot)
    avg_each_season4.append(tot/tot_team[i-2018])

fig=plt.figure()
plt.plot(range(2008,2020),tot_each_season4,label = 'total 4s')
plt.plot(range(2008,2020),moving_avg(tot_each_season4),label = 're-built')
plt.xlabel('Year')
plt.ylabel('No of fours')
plt.title('Total number of 4s each season')
plt.legend()
plt.grid()
plt.show()

fig=plt.figure()
plt.plot(range(2008,2020),avg_each_season4,label = 'average 4s')
plt.plot(range(2008,2020),moving_avg(avg_each_season4),label = 're-built')
plt.xlabel('Year')
plt.ylabel('No of fours')
plt.title('Average number of 4s each season')
plt.legend()
plt.grid()
plt.show()

# Expected Number of Fours this season
avg = sum(tot_each_season4)/len(tot_each_season4)
avg = avg + 0.5*(tot_each_season4[-1] - moving_avg(tot_each_season4)[-1])
print('Expected Number of total fours: ',round(avg))

avg = sum(avg_each_season4)/len(avg_each_season4)
avg = avg + 0.5*(avg_each_season4[-1] - moving_avg(avg_each_season4)[-1])
print('Expected Number of average fours: ',round(avg))




s='Result-Most-Sixes-'
tot_team = [8,8,8,10,9,9,8,8,8,8,8,8]
tot_each_season6 = []; avg_each_season6 = []
for i in range(2008,2020):
    df=pd.read_csv(s+str(i)+'.csv')
    tot = total(df,'6s')
    tot_each_season6.append(tot)
    avg_each_season6.append(tot/tot_team[i-2018])

fig=plt.figure()
plt.plot(range(2008,2020),tot_each_season6,label = 'total 6s')
plt.plot(range(2008,2020),moving_avg(tot_each_season6),label = 're-built')
plt.xlabel('Year')
plt.ylabel('No of sixes')
plt.title('Total number of 6s each season')
plt.grid()
plt.legend()
plt.show()

fig=plt.figure()
plt.plot(range(2008,2020),avg_each_season6,label = 'average 6s')
plt.plot(range(2008,2020),moving_avg(avg_each_season6),label = 're-built')
plt.grid()
plt.xlabel('Year')
plt.ylabel('No of sixes')
plt.title('Average number of 6s each season')
plt.legend()
plt.show()

# Expected Number of Sixes this season
avg = sum(tot_each_season6)/len(tot_each_season6)
avg = avg + 0.5*(tot_each_season6[-1] - moving_avg(tot_each_season6)[-1])
print('Expected Number of total sixes: ',round(avg))

avg = sum(avg_each_season6)/len(avg_each_season6)
avg = avg + 0.5*(avg_each_season6[-1] - moving_avg(avg_each_season6)[-1])
print('Expected Number of average sixes: ',round(avg))