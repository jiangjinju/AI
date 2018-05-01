import random
import pdb
import copy
import time
import signal

class Gobblet(object):

	def __init__(self, color= -1, size = -1, copy=None):
		if not copy:
			self.color = color
			self.size = size
		else:
			#Copy constructor
			self.color = copy.color
			self.size = copy.size

	def __str__(self):
		return "(color: {c}, size: {s})".format(c=self.color, s=self.size)

	def __repr__(self):
		if self.color == -1 and self.size == -1:
			return "(free)"
		else:
			return "(color: {c}, size: {s})".format(c=self.color, s=self.size)

	def dummy(self):
		"""
		Returns true when a gobblet is dummy (size -1 and color -1)
		or false otherwise
		"""
		if self.color == -1 and self.size == -1:
			return True
		return False

class PegStack(object):
	def __init__(self, big_peg, medium_peg, small_peg, tiny_peg):
		"""
		Initializer
		"""
		self.stack=list()
		self.stack.append(tiny_peg)
		self.stack.append(small_peg)
		self.stack.append(medium_peg)
		self.stack.append(big_peg)

	def __str__(self):
		"""
		Prints the stack to the display
		"""
		s = ""
		for i in range(0, len(self.stack)):
			s = s + str(self.stack[i]) + "\n"
		return s

	def __iter__(self):
		for peg in self.stack:
			yield peg

	def pop(self):
		"""
		Pops the top gobblet from the stack
		"""
		return self.stack.pop()

	def top(self):
		"""
		Return the top gobblet in the stack
		"""
		return self.stack[len(self.stack)-1]


	def get_top_size(self):
		"""
		Returns the size of the top gobblet in the stack
		"""
		return self.stack[len(self.stack)-1].size


class Square(object):
	"""
	This class represents a Square on the board
	"""

	def __init__(self):
		self.stack = list()
		for i in range(0,3):
			self.stack.append(Gobblet())

	def __str__(self):
		return str(self.stack)

	def __repr__(self):
		return str(self.stack)

	def full(self):
		for i in range(0,3):
				if self.stack[i].dummy():
					return False
		return True

	def empty(self):
		"""
		Returns true if a square is empty or false otherwise
		"""
		return self.stack[0].dummy()


#create gobbletboard
def gobbletboard():
    gobbletb=[[[] for x in range(4)] for y in range(4)]
    return gobbletb

#check whether one wins
def check_win(gobbletb):
    #get the top peg player
    primex=[[-1 if gobbletb[x][y]==[] else max(gobbletb[x][y])[1] for x in range(4)] for y in range(4)]
    primey=[[-1 if gobbletb[x][y]==[] else max(gobbletb[x][y])[1] for y in range(4)] for x in range(4)]
    #check horizontal/vertical lines
    for i in range(4):
        if primex[i].count(0)==4 or primey[i].count(0)==4:
            return 0
        if primex[i].count(1)==4 or primey[i].count(1)==4:
            return 1
    #check diagnal & antidiagnal
    dgn=[primex[x][x] for x in range(4)]
    antidgn=[primex[x][3-x] for x in range(4)]
    if dgn.count(0)==4 or antidgn.count(0)==4:
        return 0
    if dgn.count(1)==4 or antidgn.count(1)==4:
        return 1
    return -1

#hvevaluate a state
def hvevaluate(gobbletb):
    #hvevaluate function
    score=0
    # get the top peg player
    primex = [[-1 if gobbletb[x][y] == [] else max(gobbletb[x][y])[1] for x in range(4)] for y in range(4)]
    primey = [[-1 if gobbletb[x][y] == [] else max(gobbletb[x][y])[1] for y in range(4)] for x in range(4)]
    for i in range(4):
        if primex[i].count(1)==0:
            score+=pow(primex[i].count(0),2)
        elif primex[i].count(0)==0:
            score-=pow(primex[i].count(1),2)
        if primey[i].count(1)==0:
            score+=pow(primey[i].count(0),2)
        elif primey[i].count(0)==0:
            score-=pow(primey[i].count(1),2)
    #check diagnoal
    dgn = [primex[x][x] for x in range(4)]
    antidgn = [primex[x][3 - x] for x in range(4)]
    if dgn.count(1) == 0:
        score += pow(dgn.count(0),2)
    elif dgn.count(0) == 0:
        score -= pow(dgn.count(1),2)
    if antidgn.count(1) == 0:
        score += pow(antidgn.count(0),2)
    elif antidgn.count(0) == 0:
        score -= pow(antidgn.count(1),2)
    return score

def move(gobbletb,pegs,action):
    #action is a tuple (player,chess,(oldx,oldy),(newx,newy))
    player=action[0]
    chess=action[1]
    oldpos=action[2]
    newpos=action[3]
    if oldpos!=(-1,-1): #and (chess,player) in gobbletb[oldpos[0]][oldpos[1]]:
        if (chess,player) not in gobbletb[oldpos[0]][oldpos[1]]:
            print("not in")
            print((chess,player))
            print(oldpos)
            print(gobbletb[oldpos[0]][oldpos[1]])
        gobbletb[oldpos[0]][oldpos[1]].remove((chess,player))
    gobbletb[newpos[0]][newpos[1]].append((chess,player))
    pegs[player][chess]=newpos

#unmove an action
def unmove(gobbletb,pegs,action):
    player = action[0]
    chess = action[1]
    oldpos = action[2]
    newpos = action[3]
    gobbletb[newpos[0]][newpos[1]].remove((chess,player))
    if oldpos!=(-1,-1):
        gobbletb[oldpos[0]][oldpos[1]].append((chess,player))
    pegs[player][chess]=oldpos

#find all possible next move
def get_move(gobbletb,player,pegs):
    mypeg=pegs[player]
    moves=[]
    for i in range(len(mypeg)):
        curr_x=mypeg[i][0]
        curr_y=mypeg[i][1]
        if (curr_x,curr_y) == (-1,-1) or max(gobbletb[curr_x][curr_y])[0]==i:
            for x in range(4):
                for y in range(4):
                    if gobbletb[x][y]==[] or max(gobbletb[x][y])[0]//4<i//4:
                        seq=(player,i,(curr_x,curr_y),(x,y))
                        moves.append(seq)
    return moves
#computer player
def computer_play(gobbletb,player,pegs,level):
    if level==0: #if level is 0, then randomly play
        return random_play(gobbletb,player,pegs)
    elif level==1:#if level is 1 or 2, using alpha_beta pruning
        _,action = alpha_beta(gobbletb,player,pegs,2)
        move(gobbletb,pegs,action)
        return True,action
    else:
        _,action=alpha_beta(gobbletb,player,pegs,3)
        move(gobbletb,pegs,action)
        return True,action

#minimax algorithm
def minimax(gobbletb,player,pegs,depth):
    if depth==0:
        return hvevaluate(gobbletb),None
    actions=get_move(gobbletb,player,pegs)
    if not actions:
        return hvevaluate(gobbletb),None
    best_score=-100000
    best_action=None

    #go over each successor
    for action in actions:
        move(gobbletb,pegs,action)
        score,_=minimax(gobbletb,1-player,pegs,depth-1)
        unmove(gobbletb,pegs,action)

        score=-score
        if score>best_score:
            best_score=score
            best_action=action

    return best_score,best_action

#alpha-beta pruning algorithm
def alpha_beta(gobbletb,player,pegs,depth,mybest=-float('inf'),oppbest=float('inf')):
    if depth==0:
        score=hvevaluate(gobbletb)
        if player==0:
            return score,None
        else:
            return -score,None
    actions=get_move(gobbletb,player,pegs)
    if not actions:
        score = hvevaluate(gobbletb)
        if player == 0:
            return score, None
        else:
            return -score, None
    best_score=mybest
    best_action=None

    for action in actions:
        move(gobbletb,pegs,action)
        score,_=alpha_beta(gobbletb,1-player,pegs,depth-1,-oppbest,-best_score)
        unmove(gobbletb,pegs,action)

        score=-score
        if score>best_score:
            best_score=score
            best_action=action

        #pruning
        if best_score>oppbest:
            break

    return best_score,best_action


def play(board, all_pegs, on_board_pegs_black, off_board_pegs_black,
         on_board_pegs_white, off_board_pegs_white,
         black_stacks, white_stacks):
    pdb.set_trace()
    if board.check_winner():
        return

    player = "White"
    res = False
    winning_move_blocker = board.three_in_a_row_ai()
    winning_move = board.three_in_a_row_ai()
    PC_winning_move = board.three_in_a_row_ai("White")
    winning_square = None
    L_blocker = board.find_L_blocker()

    # First move- put one large peg on a random square
    if len(on_board_pegs_black) == 0:

        peg_number = randint(1, 3)
        res = False

        peg_object = black_stacks[peg_number - 1].top()

        # Get peg name
        for key, value in all_pegs.iteritems():
            if value == peg_object:
                peg_name = key

        # Make a random move as a begining. The while loop is in case
        # the move is not valid
        while not res:
            i = randint(0, 3)
            j = randint(0, 3)

            # Perform move
            res = board.place_gobblet_on_sqaure(i, j, all_pegs[peg_name])

        # Check for winner
        winner = board.check_winner()

        # Return JSON
        data = dict()
        data['result'] = res;
        data['peg_name'] = peg_name;
        data['square'] = str(i) + str(j)
        data['winner'] = winner
        data['new_peg'] = True
        return data

    # Case that PC has a winning move
    if PC_winning_move:
        if PC_winning_move.has_key('row'):
            PC_winning_square = PC_winning_move['row']
            dont_move = PC_winning_square[0]
            direction = "row"
        elif PC_winning_move.has_key('col'):
            PC_winning_square = PC_winning_move['col']
            dont_move = PC_winning_square[1]
            direction = "col"
        elif PC_winning_move.has_key('diag'):
            PC_winning_square = PC_winning_move['diag']

        # Get winning square and opponent peg data
        i = PC_winning_square[0]
        j = PC_winning_square[1]
        opponent_peg_size = board.grid[i][j].stack[
            board.find_top_peg_on_square(PC_winning_square[0], PC_winning_square[1])].size
        opponent_peg_color = board.grid[i][j].stack[
            board.find_top_peg_on_square(PC_winning_square[0], PC_winning_square[1])].color

        # Case the winning square is empty- posible to place new peg
        if board.grid[i][j].stack[board.find_top_peg_on_square(i, j)].size == -1:
            peg = black_stacks[get_biggest_peg_possible(black_stacks)].top()

            for key, value in all_pegs.iteritems():
                if peg is value:
                    peg_name = key
            res = board.place_gobblet_on_sqaure(PC_winning_square[0], PC_winning_square[1], peg)

            if res:
                data = dict()
                data['result'] = res
                data['peg_name'] = peg_name;
                data['square'] = str(PC_winning_square[0]) + str(PC_winning_square[1])
                data['winner'] = board.check_winner()
                data['new_peg'] = True
                return data

        # Re-position peg on the board to win without breaking the 3 in a row
        elif opponent_peg_size != 4 and len(on_board_pegs_black) > 3:
            if direction == "row" or direction == "col":
                peg = None
                current_i = None
                current_j = None
                for i in range(0, 4):
                    for j in range(0, 4):
                        if (i != dont_move and direction == "row") or (
                                j != dont_move and direction == "col") and not peg:
                            current_peg = board.grid[i][j].stack[board.find_top_peg_on_square(i, j)]
                            if current_peg.size > opponent_peg_size and current_peg.color == "Black":
                                peg = board.grid[i][j].stack[board.find_top_peg_on_square(i, j)]
                                current_i = i
                                current_j = j

            # Get peg name
            for key, value in on_board_pegs_black.iteritems():
                if peg is value:
                    peg_name = key

            # Perform move
            res = board.move_peg_on_board(current_i, current_j, PC_winning_square[0], PC_winning_square[1])

            if res:
                data = dict()
                data['result'] = res
                data['peg_name'] = peg_name;
                data['square'] = str(PC_winning_square[0]) + str(PC_winning_square[1])
                data['winner'] = board.check_winner()
                data['new_peg'] = False
                return data

    if winning_move:
        if winning_move.has_key('row'):
            if board.grid[winning_move['row'][0]][winning_move['row'][1]].stack[
                board.find_top_peg_on_square(winning_move['row'][0], winning_move['row'][1])].color != "Black":
                winning_square = winning_move['row']
                forbidden = winning_square[0]

        if winning_move.has_key('col'):
            if board.grid[winning_move['col'][0]][winning_move['col'][1]].stack[
                board.find_top_peg_on_square(winning_move['col'][0], winning_move['col'][1])].color != "Black":
                winning_square = winning_move['col']
                forbidden = winning_square[1]

        if winning_move.has_key('diag'):
            if board.grid[winning_move['diag'][0]][winning_move['diag'][1]].stack[
                board.find_top_peg_on_square(winning_move['diag'][0], winning_move['diag'][1])].color != "Black":
                winning_square = winning_move['diag']

    if winning_square:
        temp = board.grid[winning_square[0]][winning_square[1]].stack[
            board.find_top_peg_on_square(winning_square[0], winning_square[1])]

        if temp.size != 4 or temp.color != 'Black':

            # Case that there are no pegs to reposition on the board- place a new peg
            found_big_peg = False
            for i in range(0, 4):
                for j in range(0, 4):

                    if (board.grid[i][j].stack[board.find_top_peg_on_square(i, j)].size == 4 and
                            board.grid[i][j].stack[board.find_top_peg_on_square(i, j)].color == "Black" and
                            not found_big_peg):
                        peg = board.grid[i][j].stack[board.find_top_peg_on_square(i, j)]
                        old_i = i
                        old_j = j
                        found_big_peg = True

            # Get peg name
            for key, value in on_board_pegs_black.iteritems():
                if peg is value:
                    peg_name = key

            res = board.move_peg_on_board(old_i, old_j, winning_square[0], winning_square[1])

            if res:
                data = dict()
                data['result'] = res
                data['peg_name'] = peg_name;
                data['square'] = str(winning_square[0]) + str(winning_square[1])
                data['winner'] = board.check_winner()
                data['new_peg'] = False

                return data



    # Block the L tactic by moving the biggest peg to the block position
    elif L_blocker:
        biggest_peg = get_biggest_peg_possible(black_stacks)

        # Case there is a large peg outside the board
        if black_stacks[biggest_peg].top().size == 4:
            peg = black_stacks[biggest_peg].pop()
            i = L_blocker[0]
            j = L_blocker[1]

            # Get peg name
            for key, value in off_board_pegs_black.iteritems():
                if peg is value:
                    peg_name = key

            # Make a move
            res = board.move_peg_on_board(i, j, peg)

            if res:
                data = dict()
                data['result'] = res
                data['peg_name'] = peg_name;
                data['square'] = str(L_blocker[0]) + str(L_blocker[1])
                data['winner'] = board.check_winner()
                data['new_peg'] = True

                return data

        # Re- place a large gobblet on the board
        else:
            found_big_peg = False
            for i in range(0, 4):
                for j in range(0, 4):

                    if (board.grid[i][j].stack[board.find_top_peg_on_square(i, j)].size == 4 and
                            board.grid[i][j].stack[board.find_top_peg_on_square(i, j)].color == "Black" and
                            not found_big_peg):
                        peg = board.grid[i][j].stack[board.find_top_peg_on_square(i, j)]
                        old_i = i
                        old_j = j
                        found_big_peg = True

            # Get peg name
            for key, value in on_board_pegs_black.iteritems():
                if peg is value:
                    peg_name = key

            res = board.move_peg_on_board(old_i, old_j, L_blocker[0], L_blocker[1])

            if res:
                data = dict()
                data['result'] = res
                data['peg_name'] = peg_name;
                data['square'] = str(L_blocker[0]) + str(L_blocker[1])
                data['winner'] = board.check_winner()
                data['new_peg'] = False

                return data

    # Play by heuristics values
    if not res:
        nodes_list_new_pegs_black = get_hv_list_for_new_pegs(black_stacks, board)
        nodes_list_replace_pegs_black = get_hv_list_for_replace_pegs(on_board_pegs_black, board, all_pegs)
        max_replace = find_max_hv(nodes_list_replace_pegs_black, "Black")
        max_new = find_max_hv(nodes_list_new_pegs_black, "Black")

        if max_replace != 100:
            max_replace_value = nodes_list_replace_pegs_black[max_replace].hv[1]
        else:
            max_replace_value = -1
        max_new_value = nodes_list_new_pegs_black[max_new].hv[1]

        # -------------------#
        # Find the best move #
        # -------------------#

        # Make a winning move if possible:
        print(winning_move)
        if winning_move:
            if winning_move.has_key("row"):
                winning_square = winning_move["row"]
            elif winning_move.has_key("col"):
                winning_square = winning_move["col"]
            elif winning_move.has_key("diag"):
                winning_square = winning_move["diag"]

            print("WINNING MOVE:")
            print(winning_move)

        if winning_move and board.grid[winning_square[0]][winning_square[1]].stack[
            board.find_top_peg_on_square(winning_square[0], winning_square[1])].color != "Black":

            # Find the biggest peg possible to add to the board
            gb = black_stacks[get_biggest_peg_possible(black_stacks)].top()

            # Get peg name
            for key, value in off_board_pegs_black.iteritems():
                if gb is value:
                    peg_name = key

            keep_looking = True
            valid_res = False
            forbidden_row = winning_square[0]
            opponent_peg_size = board.grid[winning_square[0]][winning_square[1]].stack[
                board.find_top_peg_on_square(winning_square[0], winning_square[1])].size

            if winning_move.has_key("diag"):
                res = board.place_gobblet_on_sqaure(winning_square[0], winning_square[1], gb)
                if res:
                    valid_res = True
                    winner = board.check_winner()

            if opponent_peg_size == 4 and not valid_res:  # Can't cover the largest peg
                winner = False
                res = False
                for i in range(0, 4):
                    for j in range(0, 4):
                        loose = True
                        board_copy = copy.deepcopy(board)

                        # Don't break the current chain of 3
                        if i != forbidden_row and (res != 1 or res != 2) and keep_looking and (
                                i != winning_square[0] and j != winning_square[1]):
                            top_peg = board.grid[i][j].stack[board.find_top_peg_on_square(i, j)]
                            loose = board.three_in_a_row(i, j, top_peg, "White")

                            # Cover opponent peg if possible
                            if top_peg.color == "Black" and top_peg.size > opponent_peg_size and not loose and (
                                    i != winning_square[0] and j != winning_square[1]):

                                res = board_copy.move_peg_on_board(i, j, winning_square[0], winning_square[1])
                                # Get peg name
                                if res != 0:
                                    for key, value in on_board_pegs_black.iteritems():
                                        if value is top_peg:
                                            peg_name = key
                                            valid_res = res
                                            keep_looking = False
                                            winner = board_copy.check_winner()

            # Return JSON to jQuery
            if valid_res:
                data = dict()
                data['result'] = valid_res
                data['peg_name'] = peg_name;
                data['square'] = str(winning_square[0]) + str(winning_square[1])
                data['winner'] = winner
                data['new_peg'] = True

                # pdb.set_trace()
                return data


#random select a possible peg to move
def random_play(gobbletb,player,pegs):
    actions=get_move(gobbletb,player,pegs)
    action=random.choice(actions)
    move(gobbletb,pegs,action)
    return True,action
class InputTimeoutError(Exception):
    pass

def interrupted(signum,frame):
    raise InputTimeoutError
#run out of time
def human_play_notimer(gobbletb,player,pegs):
    mypeg=pegs[player]
    chess = int(input("which one do you want to move?"))
    oldpos = mypeg[chess]
    print("The old position of " + str(chess) + " is " + str(oldpos))
    if oldpos != (-1, -1) and max(gobbletb[oldpos[0]][oldpos[1]])[1] != player:
        print("This chess is covered by another!!")
        return False,()
    newpos = input("Which position do you want to put this chess? x,y ").split(",")
    newx = int(newpos[0])
    newy = int(newpos[1])
    if gobbletb[newx][newy] != [] and max(gobbletb[newx][newy])[0] // 4 >= chess // 4:
        print("This position is ocpegied!!!")
        return False,()
    seq = (player, chess, oldpos, (newx, newy))
    move(gobbletb, pegs, seq)
    return True, seq

def human_play(gobbletb,player,pegs,time):
    mypeg=pegs[player]
    signal.signal(signal.SIGALRM,interrupted)
    signal.alarm(time*60)
    try:
        while True:
            chess=int(input("which chess do you want to move?"))
            oldpos=mypeg[chess]
            print("The old position of "+str(chess)+" is "+str(oldpos))
            if oldpos!=(-1,-1) and max(gobbletb[oldpos[0]][oldpos[1]])[1]!=player:
                print("This chess is covered by another!!")
                continue
            newpos=input("Which position do you want to put this chess? x,y ").split(",")
            newx=int(newpos[0])
            newy=int(newpos[1])
            if gobbletb[newx][newy]!=[] and max(gobbletb[newx][newy])[0]//4>=chess//4:
                print("This position is ocpegied!!!")
                continue
            seq=(player,chess,oldpos,(newx,newy))
            move(gobbletb,pegs,seq)
            return True,seq
    except InputTimeoutError:
        return random_play(gobbletb,player,pegs)


def gobby(type,level,time):
    #initial gobbletboard
    gobbletb=gobbletboard()

    #create lists to memorize position of each peg
    pegs=[[(-1,-1)]*12,[(-1,-1)]*12]

    #get type
    player0=type[0]
    player1=type[1]

    #store move sequence
    move_sequence=[]

    while True:
        #keep old state
        old_state=str(gobbletb)
        #player 0 plays
        print(player0,"'s turn to play")
        if player0=="h": #human
            while True:
                succ, seq = human_play_notimer(gobbletb, 0, pegs)
                if succ:
                    break
        else:
            succ,seq=computer_play(gobbletb,0,pegs,level)
        print("player:",seq[0],"using peg:",seq[1],"moving from:",seq[2],"to:",seq[3])
        move_sequence.append(seq)

        #player 1 plays
        print(player1,"'s turn to play:")
        if player1=="h":
            while True:
                succ,seq=human_play_notimer(gobbletb,1,pegs)
                if succ:
                    break
        else:
            succ,seq=computer_play(gobbletb,1,pegs,level)
        print("player:", seq[0], "using peg:", seq[1], "moving from:", seq[2], "to:", seq[3])
        move_sequence.append(seq)

        if old_state==str(gobbletb):
            print("draw!!!")
            return move_sequence,-1
        winner=check_win(gobbletb)
        if winner!=-1:
            print("player "+str(winner)+" wins")
            return move_sequence, winner

gobby("rr",3,18)