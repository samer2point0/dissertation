import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import itertools
import copy
import sampling
import random
import math
from scipy import stats


FuncList=['noSeed', 'randseed', 'degree', 'degDisc', 'MPG','CHD','degN', 'voteQ']
SetupList=[[0.02,0.05], [[2,0.5], [5,0.2]], [250]]

def ttest(gName, exp1, exp2):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')

    exp1=str(exp1)
    exp2=str(exp2)
    l1=DF[exp1].dropna().tolist()
    l2=DF[exp2].dropna().tolist()

    t=[x for x in list(stats.ttest_ind(l1, l2))]
    return t[1]

def ttests(gName, Fex, slist=SetupList, flist=FuncList):
    fflist=list(itertools.product(flist, repeat=2))
    sslist=list(itertools.product(*slist))
    tL=[]
    ffex=[x for x in itertools.product(Fex, repeat=2) if x[0]!=x[1]]
    for ff in ffex:
        expL=[]
        for s in sslist:
            for ffpair in fflist:
                exp1=[ffpair[0], ffpair[1], s[0], s[1], s[2]]
                if not exp1 in expL:
                    if ff[0] in ffpair:
                        exp2=copy.deepcopy(exp1)
                        exp2=[ff[1] if x == ff[0] else x for x in exp2]
                    if ff[1] in ffpair:
                        exp2=copy.deepcopy(exp1)
                        exp2=[ff[0] if x == ff[1] else x for x in exp2]
                    if (ff[0] in ffpair or ff[1] in ffpair):
                        #print(exp1)
                        #print(exp2)
                        #print(ttest(gName, exp1, exp2))
                        expL.extend([exp1,exp2])
                        tL.append(ttest(gName, exp1, exp2))
    s=0
    for p in tL:
        if p>=0.05:
            s=s+1
    print(len(tL),s)

def drawN(g, sub, col=['#dbb844'],pos=None):
    #takes graph, list of sub node lists, and list of colors
    if pos==None:
        pos=nx.spring_layout(g)
    dcol='black'
    nL=list(g.nodes())
    cL=[dcol]*len(nL)
    for i in range(0,len(sub)):
        nL.extend(sub[i])
        cL.extend([col[i]]*len(sub[i]))

    nx.draw(g, nodelist=nL, node_color=cL, with_labels=False, pos=pos, node_size=20, width=0.1)
    plt.show()
    return pos

def drawNsmp(g, sample, sub, size=100, col=None, pos=None):#graogh, set or list, list of sets, ..
    G=g.subgraph(sample)
    for i in range(0,len(sub)):
        sub[i]=list(sub[i].intersection(sample))

    pos=drawN(G, sub, col=col, pos=pos)
    return pos

def matrix(gName, flist=FuncList, slist=SetupList):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')
    fflist=list(itertools.product(flist, repeat=2))
    sslist=list(itertools.product(*slist))
    L=[]
    for s in sslist:
        m=pd.DataFrame(numpy.zeros((len(flist),len(flist))), columns=flist, index=flist)
        std=pd.DataFrame(numpy.zeros((len(flist),len(flist))), columns=flist, index=flist)
        for ffpair in fflist:
            c=str([ffpair[0], ffpair[1], s[0], s[1], s[2]])
            if c in DF.columns:
                #col boost and rows inH
                m[ffpair[0]].loc[ffpair[1]]=DF[c].mean()
                std[ffpair[0]].loc[ffpair[1]]=DF[c].std()

        print('\n\nBellow are the mean and std matrix for the set up \n',c)
        print(m,'\n\n', std)
        L.append([m,std])

    return L, sslist

def vsMat(gName, flist=FuncList, slist=SetupList):
    L=[]
    DF=pd.read_csv('./tests/'+gName+'_test.txt')
    fflist=list(itertools.product(flist, repeat=2))
    sslist=list(itertools.product(*slist))
    i=0
    d=0
    W=dict(zip(flist,[0]*len(flist)))
    for s in sslist:
        tDF=pd.DataFrame(numpy.zeros((len(flist),len(flist))), columns=flist, index=flist)
        for (f1,f2) in fflist:
            c1=str([f1, f2, s[0], s[1], s[2]])
            c2=str([f2, f1, s[0], s[1], s[2]])
            l1=DF[c1].dropna().tolist()
            l2=DF[c2].dropna().tolist()

            t=[round(x,3) for x in list(stats.ttest_ind(l1, l2))]
            tDF[f1].loc[f2]=str(t)
            if t[1]<0.05 and t[0]>0:
                W[f1]=W[f1]+1

        print('\n\nBellow are the VS t-tests for the set up \n',sslist[i])
        print(tDF)
        L.append(DF)
        i=i+1

    print(W)

    return L ,sslist

def plotExp(gName, xAx,FC='inH', FB=FuncList, FinH=FuncList, slist=SetupList):
    xi = 0 if xAx=='PP' else 1 #seedsize Excluded
    tempslist=copy.deepcopy(slist)
    del tempslist[xi]
    sslist=list(itertools.product(*tempslist))
    DF=pd.read_csv('./tests/'+gName+'_test.txt')

    Fconst=FB if FC=='B' else FinH
    Fchang=FinH if FC=='B' else FB
    for s in sslist:
        fig=plt.figure(figsize=(300,20))
        fig.gca().set_xticks([])
        fig.gca().set_yticks([])
        ax=fig.subplots(len(Fconst), 1, squeeze=False)
        for i in range(len(Fconst)):
            for j in range(len(Fchang)):
                print('runss')
                x,y,yerr=[],[],[]
                for z in range(len(slist[xi])):
                    stemp=list(s)
                    stemp.insert(xi, slist[xi][z]) #replace with slist if necassary
                    xtemp=slist[xi][z] if xAx=='PP' else slist[xi][z][0]
                    x.append(xtemp)


                    b=i if FC=='B' else j
                    h=j if FC=='B' else i
                    c=str([FB[b], FinH[h], stemp[0], stemp[1], stemp[2]])
                    y.append(DF[c].mean())
                    yerr.append(DF[c].std())
                ax[i,0].errorbar(x, y, yerr=yerr,  label=Fchang[j], linewidth=3)
            maxX, maxS=max(x), max(y)+max(yerr)
            minX, minS=min(x), min(y)+max(yerr)
            ax[i,0].title.set_text('Competing against '+FinH[h])
            ax[i,0].set_ylabel('Mean target counts')
        ax[i,0].set_xlabel('Influence ratio of boosting concept r(T,B)')

        plt.legend(loc='lower right')
        plt.show()

def plotAtr(gName, a, FC='inH',slist=SetupList, FB=FuncList, FinH=FuncList):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')

    tempslist=copy.deepcopy(slist)
    del tempslist[a]
    sslist=list(itertools.product(*tempslist))

    Fconst=FB if FC=='B' else FinH
    Fchang=FinH if FC=='B' else FB

    for setup in slist[a]:
        for i in range(len(Fconst)):
            size=8
            fig=plt.figure(figsize=(size,size))
            assend=numpy.linspace(0, size, size)
            const=numpy.full((size,0),size)

            colors=['sienna','lime','g','c','y', 'm', 'r','b','grey']
            M=[]
            for j,fch in enumerate(Fchang):
                L=[]
                for z,x in enumerate(sslist):
                    x=list(x)
                    x.insert(a, setup)
                    b=i if FC=='B' else j
                    h=j if FC=='B' else i
                    c=str([FB[b], FinH[h], x[0], x[1], x[2]])
                    l=DF[c].dropna().tolist()
                    L.append(l)
                M.append(L)

            mini,maxi=[],[]
            l=len(sslist)
            for j,fch in enumerate(Fchang):
                c=colors.pop()
                btheta=-3.1415/8
                for z,x in enumerate(sslist):
                    thetaInc=btheta+j*3.1415/len(Fchang)/4
                    r=M[j][z]
                    theta=[z*3.1415*2/l+thetaInc+btheta*random.random()/len(Fchang) for x in r]
                    label=fch if z==0 else None
                    plt.polar(theta, r,color=c,marker='o', ls=' ', ms=3, label=label)
                    plt.polar([3.1415/l+z*3.1415/(l/2)]*2, [0,31000],'-k')
                    plt.polar([theta.pop()], [sum(r)/len(r)], 'xk')
                    maxi.append(max(r))

            maxi=max(maxi)
            plt.title('Graph '+gName +' with seedsize '+str(setup)+ ' and '+ FC+' functin '+ str(Fconst[i]))
            ax=fig.gca()
            ax.set_rmax( maxi+100)
            ticks=[str(sslist[int(x)]) for x in range(l)]
            d={'fontsize': 12,'fontweight': 'bold'}
            ax.set_xticks([(x*3.1415/(l/2)) for x in range(l)])
            ax.set_xticklabels(ticks, fontdict=d)
            plt.legend(loc='lower right')
            plt.show()

def hist(gName, Exps):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')

    fig=plt.figure()
    labels=['PP=0.01 & r(T,B)=1.25', 'PP=0.05 & r(T,B)=1.25', 'PP=0.05 & r(T,B)=5']
    i=0
    for x in Exps:
        exp=str(x)
        l=stats.zscore(DF[exp].dropna().tolist())
        plt.hist(l, bins=6, histtype='step',  label=exp)
        i=i+1

    ax=fig.gca()
    ax.set_xlabel('Z-scores of the target counts')
    ax.set_ylabel('Frequency')
    plt.title('Normalised histogram of random boosting seed set')
    plt.legend(loc='upper right')
    plt.show()



#flist=['noSeed', 'randseed', 'degree', 'degDisc', 'MPG','CHD','degN', 'voteQ']
slist=[[0.01, 0.02,0.05], [[1.25,0.8],[2,0.5], [5, 0.2]],[250]]
matrix('astroph')
#vsMat('dblp_mhda_smp')
#plotExp('astroph', 'PP', FC='inH',FB=['cutdeg','degree'], FinH=['degN'])
#plotAtr('astroph',2 , slist=slist, FC='B')
#x=ttest('dblp_mhda_smp', ['MPG', 'voteQ',0.02, [2,0.5], 250],['CHD', 'voteQ',0.02, [2,0.5], 250])
#print(x)
#ttests('dblp_mhda_smp', ['CHD', 'MPG'], slist=[[ 0.02], [[2,0.5], [5, 0.2]],[250]])
#hist('astroph', [ ['randseed', 'randseed',0.01, [1.25,0.8], 250],['randseed', 'randseed',0.05, [1.25,0.8], 250],['randseed', 'randseed',0.01, [5,0.2], 250]])
#hist('dblp_snow_smp', [ ['randseed', 'randseed',0.02, [2,0.5], 250],['randseed', 'randseed',0.05, [2,0.5], 250],['randseed', 'randseed',0.02, [5,0.2], 250]])
#hist('dblp_mhda_smp', [ ['randseed', 'randseed',0.02, [2,0.5], 250],['randseed', 'randseed',0.05, [2,0.5], 250],['randseed', 'randseed',0.02, [5,0.2], 250]])
