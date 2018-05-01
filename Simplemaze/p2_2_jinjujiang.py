# Elements of AI_Hw1_The Drone RPS game
#The following is python code provided by instructor
def rps_game(numberofgame):
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

    gamehistory =[]

    while totgames < nogames:
        #rn.seed(2018)
        if(len(gamehistory)==0):
             Robby= rn.randrange(0,3,1)
        else:
            most_common,num_most_common = Counter(gamehistory).most_common(1)[0]
            Robby=ws[most_common]
        comp = rn.randrange(0,3,1)
        gamehistory.append(comp)
        

         #print("Human: {0}, Comp: {1}".format(human, comp))

        if ws[comp] == Robby:
            compwins += 1
        elif ws[Robby] == comp:
            humwins += 1
        else:
            ties += 1
        totgames += 1

    v = list(map(lambda x: 100*x/totgames, [compwins, humwins, ties]))
    #print(gamehistory)
    #print(Counter(gamehistory[:][1]))
   # print("Stats\ncw% = {0}, hm% = {1}, ties% = {2}".format(*v))
    return (humwins,compwins,ties)
H=[]
C=[]
T=[]
n=50
sumwinh=0
sumwinc=0
sumwint=0
for i in range(n):
    h,c,t=rps_game(10)
    H.append(h)
    sumwinh +=h
    C.append(c)
    sumwinc +=c
    T.append(t)
    sumwint +=t
#print("computer wins:",C,"human wins:",H,"ties:",T)
v = list(map(lambda x: x/n, [sumwinc, sumwinh, sumwint]))
print("ncw E= {0}, Robby E = {1}, ties E = {2}".format(*v))
