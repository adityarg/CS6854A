import csv
import numpy as np
import pandas as pd
import urllib.parse
import sys
import re

################################################
file=open("articles.tsv")
df = csv.reader(file, delimiter="\t")

art=[]
for r in df:
    if len(r):
        art.append(urllib.parse.unquote(r[0]))
    else:
        art.append('')
del art[0:12]

name=[]
for r in range(len(art)):
    if r+1<10:
        name.append('A000'+str(r+1))
    elif r+1<100:
        name.append('A00'+str(r+1))
    elif r+1<1000:
        name.append('A0'+str(r+1))
    else:
        name.append('A'+str(r+1))

data= {'Code':name, 'Article':art}
df=pd.DataFrame(data,columns=['Code','Article'])

df.to_csv('article-ids.csv')


################################################
file=open("categories.tsv")
df = csv.reader(file, delimiter="\t")

cat=[]
for r in df:
    cat.append(r)
del cat[0:13]

heir=[[],[],[],[]]
for r in cat:
    s=r[1].split('.')
    for i in range(len(s)):
        if s[i] not in heir[i]:
            heir[i].append(urllib.parse.unquote(s[i]))

for i in range(4):
    heir[i].sort()

c=1
df=pd.DataFrame(columns=['Code','Category'])
for i in range(4):
    for j in range(len(heir[i])):
        if c<10:
            nr = {'Code':heir[i][j], 'Category':'C000'+str(c)}
        elif c<100:
            nr = {'Code':heir[i][j], 'Category':'C00'+str(c)}
        elif c<1000:
            nr = {'Code':heir[i][j], 'Category':'C0'+str(c)}
        else:
            nr = {'Code':heir[i][j], 'Category':'C'+str(c)}
        c+=1
        df=df.append(nr,ignore_index=True)

df.to_csv('category-ids.csv')


################################################
yup={}

df=pd.read_csv('category-ids.csv',index_col=0)
cat_code={}
for i in df.index:
    cat_code[df['Code'][i]]=df['Category'][i]

df=pd.read_csv('article-ids.csv',index_col=0)
art_code={}
for i in df.index:
    art_code[df['Article'][i]]=df['Code'][i]
    yup[df['Code'][i]]=[]

file=open("categories.tsv")
df = csv.reader(file, delimiter="\t")
cat=[]
for r in df:
    cat.append(r)
del cat[0:13]
for r in cat:
    s=r[1].split('.')
    for i in range(len(s)):
        yup[art_code[urllib.parse.unquote(r[0])]].append(cat_code[urllib.parse.unquote(s[i])])

df1=pd.DataFrame(columns=['Articles','Categories'])
for a1,a2 in yup.items():
    s='No_Category'
    for r in range(len(a2)):
        if r==0:
            s=a2[r]
        else:
            s=s+','+a2[r]
    nr = {'Articles':a1, 'Categories':s}
    df1=df1.append(nr,ignore_index=True)

df1.to_csv('article-categories.csv')


################################################
file = open("shortest-path-distance-matrix.txt","r")
text = file.readlines()
del text[0:17]

df=pd.read_csv('article-ids.csv',index_col=0)
art_code=[]
for i in df.index:
    art_code.append(df['Code'][i])

adj=[] # adjacency list
for i in art_code:
    adj.append([])
# edge={} # only edges
fe=[]; te=[];# seperated
for i in range(len(art_code)):
    for j in range(len(art_code)):
        if text[i][j]!='1':
            continue
        # edge[i]=j
        adj[i].append(j)
        fe.append(art_code[i])
        te.append(art_code[j])

df=pd.DataFrame()
df['From Article']=fe
df['To Article']=te
df.to_csv('edges.csv')
file.close()


################################################
# To increase recursion limit
sys.setrecursionlimit(5000)

def dfs(vis,stack,i):
    vis[i]=True
    for j in adj[i]:
        if vis[j]==False:
            dfs(vis,stack,j)
            stack.append(j)

def dfsUtil(vis,vn,i):
    vis[i]=True
    vn.append(i)
    for j in adj[i]:
        if vis[j]==False:
            dfs(vis,vn,j)

stack=[]
vis=[False]*len(adj)
for i in range(len(adj)):
    if vis[i]==False:
        dfs(vis,stack,i)

vis=[False]*len(adj)
ssc=[]
while len(stack)>0:
    v=stack.pop()
    if vis[v]==False:
        vn=[]
        dfsUtil(vis,vn,v)
        ssc.append(vn)

file = open("shortest-path-distance-matrix.txt","r")
text = file.readlines()
del text[0:17]

print('Number of connected components is ', len(ssc))

df=pd.DataFrame(columns=['Number of nodes','Number of edges','Diameter'])
for nodes in ssc:
    # number of nodes
    n=len(nodes)
    # number of edges
    c=0
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            # if i!=j and edge[nodes[i]]==nodes[j]:
            if j in adj[i]:
                c+=1
    # diameter
    dia=0
    for i in nodes:
        for j in nodes:
            if text[i][j]>='1' and text[i][j]<'9':
                dia=max(dia,int(text[i][j]))

    nr={'Number of nodes': n,'Number of edges': c,'Diameter': dia}
    df=df.append(nr,ignore_index=True)

df.to_csv('graph-components.csv')


################################################
file=open("paths_finished.tsv")
df = csv.reader(file, delimiter="\t")

fin=[]
for r in df:
    if len(r)==5:
        fin.append(urllib.parse.unquote(r[3]))

df=pd.read_csv('article-ids.csv',index_col=0)
art_code={}
for i in df.index:
    art_code[df['Article'][i]]=i

hpath1=[]; hpath2=[]; spath=[]; ratio1=[]; ratio2=[]
for s in fin:
    s=s.split(';')
    hpath1.append(len(s))
    c=0
    for h in s:
        if h!='<':
            c+=1
    hpath2.append(c)

    i=art_code[s[0]]; j=art_code[s[-1]]
    if text[i][j]!='_':
        spath.append(int(text[i][j])+1)
    else:
        spath.append(np.inf)
    if spath[-1]==0:
        ratio1.append(np.inf); ratio2.append(np.inf)
    else:
        ratio1.append(hpath1[-1]/spath[-1]); ratio2.append(hpath2[-1]/spath[-1])

df1=pd.DataFrame();
df1['Length of Human Path']=hpath1
df1['Length of Shortest Path']=spath
df1['Ratio of Human to Shortest Path']=ratio1
df1.to_csv('finished-paths-back.csv')

df2=pd.DataFrame();
df2['Length of Human Path']=hpath2
df2['Length of Shortest Path']=spath
df2['Ratio of Human to Shortest Path']=ratio2
df2.to_csv('finished-paths-no-back.csv')


################################################
df1=pd.DataFrame(); df2=pd.DataFrame()
c1=0; c2=0; l10=0; l11=0; r10=0; r11=0
for i in range(len(hpath1)):
    if hpath1[i]==spath[i]:
        c1+=1
    if hpath2[i]==spath[i]:
        c2+=1
    if abs(hpath1[i]-spath[i])>=1 and abs(hpath1[i]-spath[i])<=10:
        l10+=1
    if abs(hpath1[i]-spath[i])>=11:
        l11+=1
    if abs(hpath2[i]-spath[i])>=1 and abs(hpath2[i]-spath[i])<=10:
        r10+=1
    if abs(hpath2[i]-spath[i])>=11:
        r11+=1

df1['Percent of human paths equal to shortest path']= [c1/len(hpath1)*100]
df1['Percent paths length 1-10 more than shortest path']= [l10/len(hpath1)*100]
df1['Percent paths length 11 more than shortest path']= [l11/len(hpath1)*100]
df1.to_csv('percentage-paths-back.csv')

df2['Percent of human paths equal to shortest path']= [c2/len(hpath2)*100]
df2['Percent paths length 1-10 more than shortest path']= [r10/len(hpath2)*100]
df2['Percent paths length 11 more than shortest path'] = [r11/len(hpath2)*100]
df = csv.reader(file, delimiter="\t")

fin=[]
for r in df:
    if len(r)==5:
        fin.append(urllib.parse.unquote(r[3]))
df2.to_csv('percentage-paths-no-back.csv')


################################################
df=pd.read_csv('article-categories.csv')
cat={}
for i in df.index:
    cat[df['Articles'][i]]=df['Categories'][i].split(',')
df=pd.read_csv('article-ids.csv',index_col=0)
art_code={}; edge={}; art=[]
for i in df.index:
    art_code[df['Article'][i]]=df['Code'][i]
    edge[df['Code'][i]]=[]
    art.append(df['Code'][i])
    # art_index[i]=df['Code'][i]

df=pd.read_csv('edges.csv')
for i in df.index:
    edge[df['From Article'][i]].append(df['To Article'][i])

def shortest_path(src,dest,par):
    g=[src]; fl=0
    while len(g)>0:
        qw=g.pop(0)
        if qw==dest:
            fl=1
            break
        for v in edge[qw]:
            par[v]=qw
            g.append(v)
    
    if fl==0: #no path
        return [-1,-1]

    e=t[-1]; c=0; g=set([])
    while par[e]!=t[0]:
        g.update(cat[e])
        c+= len(cat[e])
        e=par[e]
    return [c,len(g)]

file=open("paths_finished.tsv")
df = csv.reader(file, delimiter="\t")
fp_r=[]; fp_Nr=[]; sp_r=[]; sp_Nr=[]; x=[]
for r in df:
    if len(r)==5:
        t=(urllib.parse.unquote(r[3])).split(";")
        t=[art_code[i] for i in t if i != '<']
        c=0; g=set([])
        for w in t:
            g.update(cat[w])
            c+= len(cat[w])
        fp_r.append(c); fp_Nr.append(len(g))
        g=set([]); g.update(cat[t[0]]); g.update(cat[t[-1]])
        sp_r.append(len(t[0])+len(t[-1])); sp_Nr.append(len(g))
        x.append(r)

df=pd.DataFrame()
df['Path']=x
df['Full Path Repeated Categories']=fp_r
df['Full Path Unique Categories']=fp_Nr
df['Shortest Path Repeated Categories']=sp_r
df['Shortest Path Unique Categories']=sp_Nr
t[-1]
df.to_csv('category-paths.csv')


################################################
df=pd.read_csv('category-ids.csv',index_col=0)
cat_count={}; cat_code={}
for i in df.index:
    cat_count[df['Category'][i]]=0
    cat_code[df['Category'][i]]=df['Code'][i]

file=open("categories.tsv")
df = csv.reader(file, delimiter="\t")
cat=[]
for r in df:
    cat.append(r)
del cat[0:13]
ding=[]
for r in cat:
    s=r[1].split('.')
    for i in reversed(range(len(s))):
        if s[i] in cat_count.keys():
            cat_count[s[i]]+= len(s)-1-i
        else:
            cat_count[s[i]]= len(s)-1-i
code=[]; sub_cat=[]
for ind in list(cat_count.keys()):
    code.append(ind)
    sub_cat.append(cat_count[ind])
df=pd.DataFrame()
df['Code']=code
df['Sub-categories']=sub_cat

df.to_csv('category-subtree-paths.csv')


################################################
