import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



df=pd.read_csv('teamwise_home_and_away.csv')

home=df['home_win_percentage'].to_numpy()
away=df['away_win_percentage'].to_numpy()

ratio = home/away
fig=plt.figure(figsize=(10,5))
plt.plot(range(len(away)),ratio)
plt.xlabel('Team Number (mentioned below)')
plt.ylabel('Ratio')
plt.grid()

for i in range(len(home)):
    print(i,'-',df['team'][i],end="; ")



low=[]; med=[]; high=[]
for i in range(len(ratio)):
    if abs(ratio[i]-1)<=0.1:
        low.append(df['team'][i])
    elif abs(ratio[i]-1)<=0.4:
        med.append(df['team'][i])
    else:
        high.append(df['team'][i])
print('Least: ',low)
print('Moderate: ',med)
print('Most: ',high)



# teams name dictionary
df=pd.read_csv('teams.csv')
ant=list(df['team1']); teams={}
for i in range(len(ant)):
    teams[ant[i]]=i
# print(len(teams))
df=pd.read_csv('matches.csv')
# df.dropna(inplace=True)
df = df[df['winner'].isnull()==False]
teams



# guii={'bat':0, 'field':1}
tosss=pd.DataFrame(columns = ['Tot_Tw','Tot_Tl','Tw_Wn','Tl_Wn','Tw_per','Tl_per'])
for i in range(15):
    nr={'Tot_Tw':0, 'Tot_Tl':0, 'Tw_Wn':0 ,'Tl_Wn':0, 'Tw_per':0, 'Tl_per':0}
    tosss=tosss.append(nr,ignore_index=True)

for k in df.index:
    i=teams[df['team1'][k]]; j=teams[df['team2'][k]]
    if teams[df['toss_winner'][k]]==i:
        tosss['Tot_Tw'][i]+=1; tosss['Tot_Tl'][j]+=1
        if teams[df['winner'][k]]==i:
            tosss['Tw_Wn'][i]+=1
        else:
            tosss['Tl_Wn'][j]+=1
    else:
        tosss['Tot_Tw'][j]+=1; tosss['Tot_Tl'][i]+=1;
        if teams[df['winner'][k]]==j:
            tosss['Tw_Wn'][j]+=1
        else:
            tosss['Tl_Wn'][i]+=1
for i in tosss.index:
    tosss['Tw_per'][i] = (tosss['Tw_Wn'][i]/tosss['Tot_Tw'][i])*100
    tosss['Tl_per'][i] = (tosss['Tl_Wn'][i]/tosss['Tot_Tl'][i])*100



t1=tosss['Tw_per'].to_numpy(); t2=tosss['Tl_per'].to_numpy()
ratio=t1/t2
fig=plt.figure(figsize=(10,5))
plt.plot(range(len(ratio)),ratio)
plt.xlabel('Teams')
plt.ylabel('Ratio')
plt.grid()

low=[]; med=[]; high=[]
for i in range(len(ratio)):
    if abs(ratio[i]-1)<=0.1:
        low.append(ant[i])
    elif abs(ratio[i]-1)<=0.6:
        med.append(ant[i])
    else:
        high.append(ant[i])
print('Least: ',low)
print('Moderate: ',med)
print('Most: ',high)




# Almost all teams won their matches when they won the match toss,
# except Mumbai Indians, Sunrisers Hydrabad, Pune Warriors, Kings XI Punjab.
# Out of which Mumbai Indians have LEAST affect and Sunrisers Hydrabad,
# Pune Warriors, Kings XI Punjab have MODERATE affect.
# Therefore, on average teams win their match when they win the toss