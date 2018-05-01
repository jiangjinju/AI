import pdb
import copy
from random import randint
import time

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


class Board(object):

	def __init__(self):
		"""
		Initializer
		"""
		self.grid = list()
		for i in range(0, 4):
			self.grid.append(list())
			for j in range(0, 4):
				self.grid[i].append(Square())

	def __str__(self):
		"""
		print function
		"""
		output = ""
		for i in range(0, 4):
			for j in range(0, 4):
				output += str(self.grid[i][j]) + " "
			output += "\n"
		return output

	def place_gobblet_on_sqaure(self, i, j, gb):
		"""
		Place a peg on the board if the move is legal
		"""

		# Make sure the square is not empty
		if self.grid[i][j].full():
			return False

		# First peg in the square- occupy if it's free'
		elif self.grid[i][j].empty():
			self.grid[i][j].stack[0] = gb
			return True

		else:
			# Find the next level to place the peg
			for k in range(1, 3):

				if self.grid[i][j].stack[k].dummy():
					# Check that the spot is valid
					# i.e not small peg on top of big peg
					if gb.size > self.grid[i][j].stack[k - 1].size:
						self.grid[i][j].stack[k] = gb
						return True

					# Case that trying to put a small peg on top of a bigger one
					else:
						return False
		return False

	def move_peg_on_board(self, old_i, old_j, new_i, new_j):
		"""
		Moves peg from (old_i, old_j) to (new_i, new_j) if the move is legal
		"""
		peg_to_move_index = self.find_top_peg_on_square(old_i, old_j)
		# Copy of the gobblet to move
		if peg_to_move_index != -1:
			new_gobblet = Gobblet(-1, -1, self.grid[old_i][old_j].stack[peg_to_move_index])

			if self.place_gobblet_on_sqaure(new_i, new_j, new_gobblet):
				# Remove the gobblet from the old location
				self.grid[old_i][old_j].stack[peg_to_move_index] = Gobblet()
				return True
		return False

	def find_top_peg_on_square(self, i, j):
		"""
		Finds the top peg on a given square
		Returns the stack level of the last peg of -1 if the square is empty
		"""
		top = -1  # Holds the top peg

		if self.grid[i][j].empty():
			return -1

		for k in range(0, 3):
			if not self.grid[i][j].stack[k].dummy():
				top = k

		return top

	def winner_row(self):
		"""
		Returns true if there is a winning row or false otherwise
		We create a list of booleans for the board rows. If there exists
		a True row then there is a winner.
		"""
		full_row = list()

		# Check if there exists a winning row
		for i in range(0, 4):
			winner = True
			for j in range(0, 3):
				# Case that the square is not empty
				if not self.grid[i][j].empty():
					# get the top gobblet on the square
					current_top_gobblet_index = self.find_top_peg_on_square(i, j)
					next_top_gobblet_index = self.find_top_peg_on_square(i, j + 1)

					# Check if gobblets have the same colors
					if self.grid[i][j].stack[current_top_gobblet_index].color != self.grid[i][j + 1].stack[
						next_top_gobblet_index].color:
						winner = False
				# Case the square is empty- impossible to be a winning row
				else:
					winner = False

			full_row.append(winner)

		return True in full_row

	def winner_col(self):
		"""
		Returns true if there is a winning column or false otherwise
		We create a list of booleans for the board columns. If there exists
		a True row then there is a winner.
		"""

		# If we have empty square on a col this col can't be a winner
		exists_empty_squares = False

		for i in range(0, 4):
			full_col = list()  # Holds the top pegs colors for the current row
			for j in range(0, 4):
				if self.grid[j][i].empty():
					exists_empty_squares = True

			if not exists_empty_squares:
				first_top_gobblet_index = self.find_top_peg_on_square(0, i)
				second_top_gobblet_index = self.find_top_peg_on_square(1, i)
				third_top_gobblet_index = self.find_top_peg_on_square(2, i)
				fourth_top_gobblet_index = self.find_top_peg_on_square(3, i)

				full_col.append(self.grid[0][i].stack[first_top_gobblet_index].color)
				full_col.append(self.grid[1][i].stack[second_top_gobblet_index].color)
				full_col.append(self.grid[2][i].stack[third_top_gobblet_index].color)
				full_col.append(self.grid[3][i].stack[fourth_top_gobblet_index].color)

				# Check that all the colors a the same
				if full_col.count(full_col[0]) == len(full_col):
					return True

			exists_empty_squares = False

		return False



"""
This class represents a state of the game
"""


class Node(object):
	def __init__(self, board_state, hv, peg_moved, destination_square_tuple, stacks, on_board_pegs=None, current_location=None):
		"""
		Initializer
		"""
		self.board = board_state
		#Heuristic value: number of options to win (white, black)
		self.hv = hv
		self.peg_moved = peg_moved
		self.destination_square = destination_square_tuple
		self.stacks = stacks
		self.on_board_pegs = on_board_pegs
		self.current_location = current_location


	def __str__(self):
		return "HV: {hv}\nPEG MOVED: {pm}\nDESTINATION: {dest}\n\n".format(hv=self.hv,
			pm=self.peg_moved,
			dest=self.destination_square)


"""
This class is the AI of the game.
All the functions is this class are to calculate heuristics values
and choose the right moves
"""




def play(board, all_pegs, on_board_pegs_black, off_board_pegs_black,
		 on_board_pegs_white, off_board_pegs_white,
		 black_stacks, white_stacks):
	pdb.set_trace()
	if board.winner_col():
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
		winner = board.winner_col()

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
				data['winner'] = board.winner_col()
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
				data['winner'] = board.winner_col()
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
				data['winner'] = board.winner_col()
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
				data['winner'] = board.winner_col()
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
				data['winner'] = board.winner_col()
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
					winner = board.winner_col()

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

		# Block the player from making a winning move

		if winning_move_blocker != False:
			if winning_move_blocker.has_key("row"):
				winning_square = winning_move_blocker["row"]
			elif winning_move_blocker.has_key("col"):
				winning_square = winning_move_blocker["col"]

			elif winning_move_blocker.has_key("diag"):
				winning_square = winning_move_blocker["diag"]

			if winning_square and not (board.grid[winning_square[0]][winning_square[1]].stack[
										   board.find_top_peg_on_square(winning_square[0],
																		winning_square[1])].color == 'Black'):

				# Find the biggest peg possible to add to the board
				gb = black_stacks[get_biggest_peg_possible(black_stacks)].top()

				# Get peg name
				for key, value in off_board_pegs_black.iteritems():
					if gb is value:
						peg_name = key

				# Perform the move
				res = board.place_gobblet_on_sqaure(winning_square[0], winning_square[1], gb)
				winner = board.winner_col()
				# Return JSON to jQuery
				if res:
					data = dict()
					data['result'] = res
					data['peg_name'] = peg_name;
					data['square'] = str(winning_square[0]) + str(winning_square[1])
					data['winner'] = board.winner_col()
					data['new_peg'] = True
					return data

		# Case that HV is greatr for placing a new peg
		if max_replace_value < max_new_value and not res:
			node = nodes_list_new_pegs_black[max_new]
			print(node.current_location)

			# Get peg name
			for key, value in off_board_pegs_black.iteritems():
				if value is node.peg_moved:
					peg_name = key

			gb = node.peg_moved

			square = node.destination_square

			res = board.place_gobblet_on_sqaure(square[0], square[1], gb)
			winner = board.winner_col()

			print("BLACK IN MOVING {pn} TO ({i}, {j})".format(pn=peg_name, i=square[0], j=square[1]))
			data = dict()
			data['result'] = res;
			data['peg_name'] = peg_name;
			data['square'] = str(square[0]) + str(square[1])
			data['winner'] = winner
			data['new_peg'] = True
			return data


		# Reposition peg on board
		elif max_replace_value >= max_new_value:

			node = nodes_list_replace_pegs_black[max_replace]
			square = node.destination_square

			current_location = node.current_location
			res = False
			loose = True
			peg_name = None

			node = nodes_list_replace_pegs_black[max_replace]
			gb = board.find_top_peg_on_square(node.current_location[0], node.current_location[1])

			# Case that the destination and the current location are the same
			while (current_location[0] == square[0] and current_location[1] == current_location[
				1]) or loose and current_location == winning_square:
				nodes_list_replace_pegs_black.remove(nodes_list_replace_pegs_black[max_replace])
				max_replace = find_max_hv(nodes_list_replace_pegs_black, "Black")
				max_replace_value = nodes_list_replace_pegs_black[max_replace].hv[1]
				node = nodes_list_replace_pegs_black[max_replace]
				square = node.destination_square
				current_location = node.current_location
				loose = current_location == winning_square

				gb = board.find_top_peg_on_square(node.current_location[0], node.current_location[1])

				# Get peg name
				for key, value in on_board_pegs_black.iteritems():  # off_board_pegs_black.iteritems():
					if value is board.grid[node.current_location[0]][node.current_location[1]].stack[gb]:
						peg_name = key

				board_copy = copy.deepcopy(board)
				res = board_copy.move_peg_on_board(current_location[0], current_location[1], square[0], square[1])

			# Case the while loop didn't execute
			if not peg_name:
				# Get peg name
				for key, value in on_board_pegs_black.iteritems():  # off_board_pegs_black.iteritems():
					if value is board.grid[node.current_location[0]][node.current_location[1]].stack[gb]:
						peg_name = key

			res = board.move_peg_on_board(current_location[0], current_location[1], square[0], square[1])

			winner = board.winner_col()

			print("BLACK IN RE-MOVING {pn} FROM ({i1},{j1}) TO ({i2}, {j2})".format(pn=peg_name, i1=current_location[0],
																					j1=current_location[1],
																					i2=square[0], j2=square[1]))
			data = dict()
			if res != 0:
				res_return = True
			else:
				res_return = False

			data['result'] = res_return;
			data['peg_name'] = peg_name;
			data['square'] = str(square[0]) + str(square[1])
			data['winner'] = winner
			data['new_peg'] = False
			# time.sleep(2)

			return data


def get_hv_list_for_new_pegs(player_stacks, board):
	"""
	Returns a list of the heuristic values for placing new pegs on the board
	"""

	nodes_list_new_pegs = list()

	for j in range(0, 3):
		biggest_peg = get_biggest_peg_possible(player_stacks)
		for i in range(0, 15):

			# Get a copy of the current board
			board_copy = copy.deepcopy(board)

			# Make a move on the board copy
			move = board_copy.place_gobblet_on_sqaure(i / 4, i % 4, player_stacks[biggest_peg].top())

			# Calculate hv
			hv_tuple = (board_copy.calculate_heuristic("White"), board_copy.calculate_heuristic("Black"))

			# Create a node for game state
			if move:
				nodes_list_new_pegs.append(
					Node(board_copy, hv_tuple, player_stacks[biggest_peg].top(), (i / 4, i % 4), player_stacks, None,
						 (i / 4, i % 4)))

	return nodes_list_new_pegs


def get_hv_list_for_replace_pegs(on_board_pegs, board, all_pegs):
	"""
	Returns a list of the heuristic values for re- placing pegs on the board
	"""
	nodes_list_replace_pegs = list()

	# pdb.set_trace()
	for peg in on_board_pegs.values():
		# get the current peg location
		# pdb.set_trace()
		board_copy = copy.deepcopy(board)

		for i in range(0, 4):
			for j in range(0, 4):
				peg_to_move_temp = board.grid[i][j].stack[board.find_top_peg_on_square(i, j)]
				if peg_to_move_temp.color == "Black":
					if peg is peg_to_move_temp:
						current_location = (i, j)
						peg_to_move = peg_to_move_temp

		for i in range(0, 4):
			for j in range(0, 4):
				board_copy = copy.deepcopy(board)
				hv_tuple = (board_copy.calculate_heuristic("White"),
							board_copy.calculate_heuristic("Black"))

				if current_location:
					move = board_copy.move_peg_on_board(current_location[0], current_location[1], i, j)

				if move == 1:
					nodes_list_replace_pegs.append(Node(board_copy, hv_tuple, peg_to_move, (i, j), None, on_board_pegs,
														(current_location[0], current_location[1])))

	return nodes_list_replace_pegs


def get_biggest_peg_possible(stacks_list):
	"""
	Returns the stack number of the biggest peg possible
	"""
	biggest = 0

	for i in range(0, 2):
		temp = stacks_list[i].top()
		if temp > biggest:
			biggest = temp
			stack_number = i
	return stack_number


def find_max_hv(nodes_list, player):
	"""
	Return the index of the highes hv in the nodes list
	"""

	if len(nodes_list) == 0:
		return 100
	elif player == "White":
		index = 0
	else:
		index = 1

	max_hv = nodes_list[0].hv[index]
	max_hv_index = 0

	for i in range(0, len(nodes_list)):
		if max_hv < nodes_list[i].hv[index]:
			max_hv = nodes_list[i].hv[index]
			max_hv_index = i

	return max_hv_index


def find_min_hv(nodes_list, player):
	"""
	Return the index of the highes hv in the nodes list
	"""
	if player == "White":
		index = 0
	else:
		index = 1

	min_hv = nodes_list[0].hv[index]
	min_hv_index = 0

	for i in range(0, len(nodes_list)):
		if min_hv > nodes_list[i].hv[index]:
			min_hv = nodes_list[i].hv[index]
			min_hv_index = i

	return min_hv_index

def gobblet(players,level,time):
	#get players
	player1=players[0]
	player2=players[1]


global pd
global ob_pd_black
global ob_pd_white
global not_ob_pd_black
global not_ob_pd_white
global black_pegs_stacks
global white_pegs_stacks
global black_stack1
global black_stack2
global black_stack3
global white_stack1
global white_stack2
global white_stack3
global mainBoard

mainBoard = Board()

# Tiny white peg
twp1 = Gobblet("White", 1);
twp2 = Gobblet("White", 1);
twp3 = Gobblet("White", 1);

# Small white peg
swp1 = Gobblet("White", 2);
swp2 = Gobblet("White", 2);
swp3 = Gobblet("White", 2);

# Medium white peg
mwp1 = Gobblet("White", 3);
mwp2 = Gobblet("White", 3);
mwp3 = Gobblet("White", 3);

# Big white peg
bwp1 = Gobblet("White", 4);
bwp2 = Gobblet("White", 4);
bwp3 = Gobblet("White", 4);

# Tiny black peg
tbp1 = Gobblet("Black", 1);
tbp2 = Gobblet("Black", 1);
tbp3 = Gobblet("Black", 1);

# Small black peg
sbp1 = Gobblet("Black", 2);
sbp2 = Gobblet("Black", 2);
sbp3 = Gobblet("Black", 2);

# Medium black peg
mbp1 = Gobblet("Black", 3);
mbp2 = Gobblet("Black", 3);
mbp3 = Gobblet("Black", 3);

# Big black peg
bbp1 = Gobblet("Black", 4);
bbp2 = Gobblet("Black", 4);
bbp3 = Gobblet("Black", 4);

'''
PEGS DICTIONARY
'''

pd = dict()

pd['twp1'] = twp1
pd['twp2'] = twp2
pd['twp3'] = twp3

pd['swp1'] = swp1
pd['swp2'] = swp2
pd['swp3'] = swp3

pd['mwp1'] = mwp1
pd['mwp2'] = mwp2
pd['mwp3'] = mwp3

pd['bwp1'] = bwp1
pd['bwp2'] = bwp2
pd['bwp3'] = bwp3

pd['tbp1'] = tbp1
pd['tbp2'] = tbp2
pd['tbp3'] = tbp3

pd['sbp1'] = sbp1
pd['sbp2'] = sbp2
pd['sbp3'] = sbp3

pd['mbp1'] = mbp1
pd['mbp2'] = mbp2
pd['mbp3'] = mbp3

pd['bbp1'] = bbp1
pd['bbp2'] = bbp2
pd['bbp3'] = bbp3

ob_pd_black = dict()
ob_pd_white = dict()
not_ob_pd_black = dict()
not_ob_pd_white = dict()

# Create dictionary for pegs on board
for key in pd.keys():
	if pd[key].color == 'Black':
		not_ob_pd_black[key] = pd[key]
	elif pd[key].color == 'White':
		not_ob_pd_white[key] = pd[key]

"""CREATE PEGS STACK"""
black_stack1 = PegStack(pd['bbp1'], pd['mbp1'], pd['sbp1'], pd['tbp1'])
black_stack2 = PegStack(pd['bbp2'], pd['mbp2'], pd['sbp2'], pd['tbp2'])
black_stack3 = PegStack(pd['bbp3'], pd['mbp3'], pd['sbp3'], pd['tbp3'])

white_stack1 = PegStack(pd['bwp1'], pd['mwp1'], pd['swp1'], pd['twp1'])
white_stack2 = PegStack(pd['bwp2'], pd['mwp2'], pd['swp2'], pd['twp2'])
white_stack3 = PegStack(pd['bwp3'], pd['mwp3'], pd['swp3'], pd['twp3'])

black_pegs_stacks = [black_stack1, black_stack2, black_stack3]
white_pegs_stacks = [white_stack1, white_stack2, white_stack3]

data1 = play(mainBoard, pd, ob_pd_black, not_ob_pd_black,
			ob_pd_white, not_ob_pd_white,
			black_pegs_stacks, white_pegs_stacks)




