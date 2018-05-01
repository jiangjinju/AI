import random

import signal

class InputTimeoutError(Exception):
    pass

def interrupted(signum,frame):
    raise InputTimeoutError

#create chessboard
def chessboard():
    cb=[[[] for x in range(4)] for y in range(4)]
    return cb

#check whether one wins
def check_win(cb):
    #get the top cup player
    dominatex=[[-1 if cb[x][y]==[] else max(cb[x][y])[1] for x in range(4)] for y in range(4)]
    dominatey=[[-1 if cb[x][y]==[] else max(cb[x][y])[1] for y in range(4)] for x in range(4)]
    #check horizontal/vertical lines
    for i in range(4):
        if dominatex[i].count(0)==4 or dominatey[i].count(0)==4:
            return 0
        if dominatex[i].count(1)==4 or dominatey[i].count(1)==4:
            return 1
    #check diagnal & antidiagnal
    dgn=[dominatex[x][x] for x in range(4)]
    antidgn=[dominatex[x][3-x] for x in range(4)]
    if dgn.count(0)==4 or antidgn.count(0)==4:
        return 0
    if dgn.count(1)==4 or antidgn.count(1)==4:
        return 1
    return -1

#evaluate a state
def eval(cb):
    #evaluate function
    #if a row has many chess for one player and no chess for another
    #its score is added by number of chess
    score=0
    # get the top cup player
    dominatex = [[-1 if cb[x][y] == [] else max(cb[x][y])[1] for x in range(4)] for y in range(4)]
    dominatey = [[-1 if cb[x][y] == [] else max(cb[x][y])[1] for y in range(4)] for x in range(4)]
    for i in range(4):
        if dominatex[i].count(1)==0:
            score+=pow(dominatex[i].count(0),2)
        elif dominatex[i].count(0)==0:
            score-=pow(dominatex[i].count(1),2)
        if dominatey[i].count(1)==0:
            score+=pow(dominatey[i].count(0),2)
        elif dominatey[i].count(0)==0:
            score-=pow(dominatey[i].count(1),2)
    #check diagnoal
    dgn = [dominatex[x][x] for x in range(4)]
    antidgn = [dominatex[x][3 - x] for x in range(4)]
    if dgn.count(1) == 0:
        score += pow(dgn.count(0),2)
    elif dgn.count(0) == 0:
        score -= pow(dgn.count(1),2)
    if antidgn.count(1) == 0:
        score += pow(antidgn.count(0),2)
    elif antidgn.count(0) == 0:
        score -= pow(antidgn.count(1),2)
    return score

#move according to an action
def move(cb,cups,action):
    #action is a tuple (player,chess,(oldx,oldy),(newx,newy))
    player=action[0]
    chess=action[1]
    oldpos=action[2]
    newpos=action[3]
    if oldpos!=(-1,-1): #and (chess,player) in cb[oldpos[0]][oldpos[1]]:
        if (chess,player) not in cb[oldpos[0]][oldpos[1]]:
            print("not in")
            print((chess,player))
            print(oldpos)
            print(cb[oldpos[0]][oldpos[1]])
        cb[oldpos[0]][oldpos[1]].remove((chess,player))
    cb[newpos[0]][newpos[1]].append((chess,player))
    cups[player][chess]=newpos

#unmove an action
def unmove(cb,cups,action):
    player = action[0]
    chess = action[1]
    oldpos = action[2]
    newpos = action[3]
    cb[newpos[0]][newpos[1]].remove((chess,player))
    if oldpos!=(-1,-1):
        cb[oldpos[0]][oldpos[1]].append((chess,player))
    cups[player][chess]=oldpos

#find all possible next move
def get_move(cb,player,cups):
    mycup=cups[player]
    moves=[]
    for i in range(len(mycup)):
        curr_x=mycup[i][0]
        curr_y=mycup[i][1]
        if (curr_x,curr_y) == (-1,-1) or max(cb[curr_x][curr_y])[0]==i:
            for x in range(4):
                for y in range(4):
                    if cb[x][y]==[] or max(cb[x][y])[0]//4<i//4:
                        seq=(player,i,(curr_x,curr_y),(x,y))
                        moves.append(seq)
    return moves

#random select a possible cup to move
def random_play(cb,player,cups):
    actions=get_move(cb,player,cups)
    action=random.choice(actions)
    move(cb,cups,action)
    return True,action

#human play without timer
def human_play_notimer(cb,player,cups):
    mycup=cups[player]
    chess = int(input("which chess do you want to move?"))
    oldpos = mycup[chess]
    print("The old position of " + str(chess) + " is " + str(oldpos))
    if oldpos != (-1, -1) and max(cb[oldpos[0]][oldpos[1]])[1] != player:
        print("This chess is covered by another!!")
        return False,()
    newpos = input("Which position do you want to put this chess? x,y ").split(",")
    newx = int(newpos[0])
    newy = int(newpos[1])
    if cb[newx][newy] != [] and max(cb[newx][newy])[0] // 4 >= chess // 4:
        print("This position is occupied!!!")
        return False,()
    seq = (player, chess, oldpos, (newx, newy))
    move(cb, cups, seq)
    return True, seq

#human play function, only works on linux
def human_play(cb,player,cups,time):
    mycup=cups[player]
    signal.signal(signal.SIGALRM,interrupted)
    signal.alarm(time*60)
    try:
        while True:
            chess=int(input("which chess do you want to move?"))
            oldpos=mycup[chess]
            print("The old position of "+str(chess)+" is "+str(oldpos))
            if oldpos!=(-1,-1) and max(cb[oldpos[0]][oldpos[1]])[1]!=player:
                print("This chess is covered by another!!")
                continue
            newpos=input("Which position do you want to put this chess? x,y ").split(",")
            newx=int(newpos[0])
            newy=int(newpos[1])
            if cb[newx][newy]!=[] and max(cb[newx][newy])[0]//4>=chess//4:
                print("This position is occupied!!!")
                continue
            seq=(player,chess,oldpos,(newx,newy))
            move(cb,cups,seq)
            return True,seq
    except InputTimeoutError:
        return random_play(cb,player,cups)

#robot play function
def robot_play(cb,player,cups,level):
    if level==0:
        return random_play(cb,player,cups)
    elif level==1:
        _,action = alpha_beta(cb,player,cups,2)
        move(cb,cups,action)
        return True,action
    else:
        _,action=alpha_beta(cb,player,cups,3)
        move(cb,cups,action)
        return True,action

#minimax algorithm
def minimax(cb,player,cups,depth):
    if depth==0:
        return eval(cb),None
    actions=get_move(cb,player,cups)
    if not actions:
        return eval(cb),None
    best_score=-100000
    best_action=None

    #go over each successor
    for action in actions:
        move(cb,cups,action)
        score,_=minimax(cb,1-player,cups,depth-1)
        unmove(cb,cups,action)

        score=-score
        if score>best_score:
            best_score=score
            best_action=action

    return best_score,best_action

#alpha-beta pruning algorithm
def alpha_beta(cb,player,cups,depth,mybest=-float('inf'),oppbest=float('inf')):
    if depth==0:
        score=eval(cb)
        if player==0:
            return score,None
        else:
            return -score,None
    actions=get_move(cb,player,cups)
    if not actions:
        score = eval(cb)
        if player == 0:
            return score, None
        else:
            return -score, None
    best_score=mybest
    best_action=None

    for action in actions:
        move(cb,cups,action)
        score,_=alpha_beta(cb,1-player,cups,depth-1,-oppbest,-best_score)
        unmove(cb,cups,action)

        score=-score
        if score>best_score:
            best_score=score
            best_action=action

        #pruning
        if best_score>oppbest:
            break

    return best_score,best_action

def gobby(type,level,time):
    #initial chessboard
    cb=chessboard()

    #create lists to memorize position of each cup
    cups=[[(-1,-1)]*12,[(-1,-1)]*12]

    #get type
    player0=type[0]
    player1=type[1]

    #store move sequence
    move_sequence=[]

    while True:
        #keep old state
        old_state=str(cb)
        #player 0 plays
        print("player 0 plays")
        if player0=="h":
            while True:
                #succ,seq=human_play(cb,0,cups,time) #On Linux
                succ, seq = human_play_notimer(cb, 0, cups) #On Windows
                if succ:
                    break
        else:
            succ,seq=robot_play(cb,0,cups,level)
        print(seq)
        move_sequence.append(seq)

        #player 1 plays
        print("player 1 plays")
        if player1=="h":
            while True:
                #succ,seq=human_play(cb,1,cups,time) #On Linux
                succ,seq=human_play_notimer(cb,1,cups)
                if succ:
                    break
        else:
            succ,seq=robot_play(cb,1,cups,level)
        print(seq)
        move_sequence.append(seq)

        #check repeated states
        if old_state==str(cb):
            print("draw!!!")
            return move_sequence,-1
        #check whether one wins
        winner=check_win(cb)
        if winner!=-1:
            print("player "+str(winner)+" wins")
            return move_sequence, winner

gobby("rr",2,10)