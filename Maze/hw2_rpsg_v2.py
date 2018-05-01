# Elements of AI_Hw1_The Drone RPS game

import pandas as pd
def rps_game(token,numberofgame):
    import random as rn

    from collections import Counter
    #values of rock, paper, scissors
    r,p,s = 0,1,2
    #dictionary e.g., rock beats scissors
    ws = {r:s, p:r, s:p}
    ws1 = {s:r, r:p, p:s}

    nogames = numberofgame

    totgames = 0
    compwins = 0
    humwins = 0
    ties = 0
    finalwage=0
    totalchipscomp=token
    totalchipsrobby=token

    gamehistory =[]

    while totgames < nogames and totalchipscomp>0 and totalchipsrobby>0:
       #rn.seed(2018)
        if(len(gamehistory)==0):
            Robby= rn.randrange(0,3,1)
        else:
            most_common,num_most_common = Counter(gamehistory).most_common(1)[0]
            Robby=ws1[most_common]
        if  totalchipsrobby==1:
            Robbywage=1
        elif totalchipscomp==1:
            Compwage=1        
        else:
            #Robbywage=rn.randrange(1,totalchipsrobby,1)
            Robbywage=1
            Compwage=rn.randrange(1,totalchipscomp,1)
        finalwage=min(Robbywage,Compwage)
        comp = rn.randrange(0,3,1)
        gamehistory.append(comp)
        

         #print("Human: {0}, Comp: {1}".format(human, comp))

        if ws[comp] == Robby:
            compwins += 1
            totalchipsrobby-=finalwage
            totalchipscomp+=finalwage
        elif ws[Robby] == comp:
            humwins += 1
            totalchipscomp-=finalwage
            totalchipsrobby+=finalwage
        else:
            ties += 1
        totgames += 1
    return (totgames,humwins,compwins,ties,totalchipsrobby,totalchipscomp)

   # v = list(map(lambda x: 100*x/totgames, [compwins, humwins, ties]))
    #print(gamehistory)
    #print(Counter(gamehistory[:][1]))
   # print("Stats\ncw% = {0}, hm% = {1}, ties% = {2}".format(*v))
    #print (humwins,compwins,ties,totalchipscomp,totalchipsrobby
n=50
res=[]
for i in range(n):
    totgames,humwins,compwins,ties,totalchipsrobby,totalchipscomp=rps_game(100,50)
    res.append((totgames,humwins,compwins,ties,totalchipsrobby,totalchipscomp))
    #print (totgames,humwins,compwins,ties,totalchipsrobby,totalchipscomp)
headerlist=('totgames','humwins','compwins','ties','totalchipsrobby','totalchipscomp') 
my_df = pd.DataFrame(res)
my_df.to_csv('out2.csv', index=False, header=headerlist)
print(my_df)