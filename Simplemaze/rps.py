import random as rn

#values of rock, paper, scissors
r,p,s = 0,1,2
#dictionary e.g., rock beats scissors
ws = {r:s, p:r, s:p}

nogames = int(input("Number of games? "))

totgames = 0
compwins = 0
humwins = 0
ties = 0

gamehistory = []

while totgames < nogames:
     human = int(input("r=0,p=1,s=2 "))
     comp = rn.randrange(0,3,1)
     gamehistory.append([human, comp])

     print("Human: {0}, Comp: {1}".format(human, comp))

     if ws[comp] == human:
        compwins += 1
     elif ws[human] == comp:
        humwins += 1
     else:
        ties += 1
     totgames += 1

v = list(map(lambda x: 100*x/totgames, [compwins, humwins, ties]))
print("Stats\ncw% = {0}, hm% = {1}, ties% = {2}".format(*v))

