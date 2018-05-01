# Elements of AI_Hw1_The Drone RPS game
#The following is python code provided by instructor
def rps_game(numberofgame):
    import random as rn

    #values of rock, paper, scissors
    r,p,s = 0,1,2
    #dictionary e.g., rock beats scissors
    ws = {r:s, p:r, s:p}

    nogames = numberofgame

    totgames = 0
    compwins = 0
    humwins = 0
    ties = 0

    gamehistory = []

    while totgames < nogames:
         human = int(input("r=0,p=1,s=2 "))
         comp = rn.randrange(0,3,1)
         gamehistory.append([human, comp])

         #print("Human: {0}, Comp: {1}".format(human, comp))

         if ws[comp] == human:
            compwins += 1
         elif ws[human] == comp:
            humwins += 1
         else:
            ties += 1
         totgames += 1

    v = list(map(lambda x: 100*x/totgames, [compwins, humwins, ties]))
   # print("Stats\ncw% = {0}, hm% = {1}, ties% = {2}".format(*v))
    return (humwins,compwins,ties)
H=[]
C=[]
T=[]
n=5
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
print("computer wins:",C,"human wins:",H,"ties:",T)
v = list(map(lambda x: x/n, [sumwinc, sumwinh, sumwint]))
print("ncw E= {0}, hm E = {1}, ties E = {2}".format(*v))