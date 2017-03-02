import math, time, random, bisect

# Puzzle Board with dim=4 for 15+1 board
# initial values -> random solvable OR totally random
# empty tile is represented with "16" for sake of simplicity
# it is printed as "X"
# Heuristic Type is Manhattan Distance by default
class PuzzleBoard:

	def __init__(self, input=None, heuristic="Manhattan"):
		self.dim_ = 4
		self.goal_tiles_ = [num for num in range(1, self.dim_**2+1)]
		if input == None:
			self.initial_tiles_ = self.findSolvableStart()
			#self.initial_tiles_ = random.sample(range(1, dim_**2+1), dim_**2)
		else:
			self.initial_tiles_ = list(input)
		if heuristic == "Manhattan":
			self.heuristic_ = "Manhattan"
		else:
 			self.heuristic_ = "MisplacedTiles"
		
			
	def isThisASolution(self, tiles):
		if self.goal_tiles_ == tiles:
			return True
		else:
			return False
			
	def findSolvableStart(self):
		tiles = list(self.goal_tiles_)
		for i in range(20):
			possible_moves = self.findPossibleMoves(tiles)
			random.shuffle(possible_moves)
			tiles = possible_moves[0]
		return tiles
			
	def findPossibleMoves(self, tiles):
		# Find the empty tile (its numeric value is "dim*dim" or "16" in our case)
		empty_tile_index = tiles.index(self.dim_**2)
		row = empty_tile_index//self.dim_
		col = empty_tile_index%self.dim_

		# Find possible moves
		moves = []
		if row > 0: 			# Empty tile is not on the first row, so we can move down!
			moves.append(empty_tile_index-self.dim_)
		if row < self.dim_-1: 		# Empty tile is not on the last row, so we can move up!
			moves.append(empty_tile_index+self.dim_)
		if col > 0: 			# Empty tile is not on the first column, so we can move right!
			moves.append(empty_tile_index-1)
		if col < self.dim_-1: 		# Empty tile is not on the last column, so we can move left!
			moves.append(empty_tile_index+1)
		
		possible_moves = []
		for m in moves:
			moved_tiles = list(tiles) # For deep copy
			# Make the move 
			moved_tiles[m], moved_tiles[empty_tile_index] = moved_tiles[empty_tile_index], moved_tiles[m]
			possible_moves.append(moved_tiles)
	
		return possible_moves
		
	def solve(self): 		# Using A* Algorithm with 2 different Heuristics
		# Use queue to keep track of the tree nodes
		# The first node of the tree (or the queue) is the initial state of the puzzle
		queued_states = [State(self.initial_tiles_, None, self)]
		popped_states = []
		counter = 0			# Count the number of nodes visited
		while True:
			current_state = queued_states.pop(0) 					# Get the first state from the queue
			counter += 1
			if self.isThisASolution(current_state.tiles_):			# Check if it is the goal state
				# Solution is found, print all the moves.
				print()
				print("Solved by using", self.heuristic_, "heuristic:", sep=" ")
				current_state.reverse()
				break
			else:
				# Find next states and add them to the queue, unless:
				# 1. They are already in the queue, queued_states
				# 2. They were once in the queue, popped_states
				popped_states.append(current_state)
				# Find possible next states (children of the current tree node)
				next_states = current_state.findNextStates()
				for state in next_states:
					if state not in popped_states and state not in queued_states:
						bisect.insort(queued_states, state)
		return counter
								
	def display(self, tiles=None):
		ctr = 1
		if tiles == None:
			tiles = self.initial_tiles_

		for tile in tiles:
			if tile != self.dim_**2:
				if (ctr%self.dim_) == 0:
					print(tile)
				else:
					print(tile, end="\t")
			else:
				if (ctr%self.dim_) == 0:
					print("X")
				else:
					print("X", end="\t")
			ctr += 1
		print("----------------------------")

# State Objects are the nodes in the expanded tree
# They hold: the current tiles,
# the parent state (the previous state),
# the last move, and
# the total cost of the current state += heuristic
class State:
	def __init__(self, tiles, previous_state, puzzle=None):
		self.tiles_ = tiles
		self.prev_ = previous_state
		self.puzzle_ = puzzle
		if puzzle == None:
			self.puzzle_ = previous_state.puzzle_
		if previous_state != None:
			self.cost_ = previous_state.cost_ + 1
		else:
			self.cost_ = 0
		
		if self.puzzle_.heuristic_ == "Manhattan":
			self.total_cost_ = self.cost_ + self.heuristicManhattan()
		else:
			self.total_cost_ = self.cost_ + self.heuristicMisplacedTiles()
		
		
	def heuristicManhattan(self):
		# Heuristic 1. -> Manhattan Distance to the goal state
		h = 0
		dim = self.puzzle_.dim_
		for x in self.tiles_:
			h += (abs(self.tiles_.index(x)//dim - self.puzzle_.goal_tiles_.index(x)//dim) + abs(self.tiles_.index(x)%dim - self.puzzle_.goal_tiles_.index(x)%dim))
		return h
	
	def heuristicMisplacedTiles(self):
		# Heuristic 2. -> The number of misplaced tiles
		h = 0
		for i in range(self.puzzle_.dim_**2):
			if self.tiles_[i] != self.puzzle_.goal_tiles_[i]:
				h += 1
		return h
	
	def findNextStates(self):
		states = []
		moved_tiles = self.puzzle_.findPossibleMoves(self.tiles_)
		for tiles in moved_tiles:
			states.append(State(tiles, self)) 
		return states
		
	def reverse(self):
		# Yay! We reached to the goal state, so let's print the tree.
		path = []
		state = State(self.tiles_, self.prev_)
		while not state.prev_ == None:
			path.append(state.tiles_)
			state = state.prev_
		path.append(state.tiles_)
		path.reverse()
		for tiles in path:
			self.puzzle_.display(tiles)
		print("Total number of moves:", len(path), sep=" ")
	
	def __eq__(self, other):
		# Override the default Equals behavior
		if isinstance(other, self.__class__):
			return self.tiles_ == other.tiles_
		return False

	def __ne__(self, other):
		# Define a non-equality test
		return not self.__eq__(other)

	def __lt__(self, other):
		# Define comparison w.r.t their estimated costs
		if isinstance(other, self.__class__):
			return self.total_cost_ < other.total_cost_
		return False

		
# Test for Manhattan Distance
P = PuzzleBoard()
P.display()
start_time = time.clock()
counter = P.solve()
end_time = time.clock()
print("Total nodes visited:", counter, sep=" ")
print("Total time:", end_time - start_time, sep=" ")


# Test the same board with number of misplaced tiles for comparison
P2 = PuzzleBoard(P.initial_tiles_, "MisplacedTiles")
#P2.display()
start_time = time.clock()
counter = P2.solve()
end_time = time.clock()
print("Total nodes visited:", counter, sep=" ")
print("Total time:", end_time - start_time, sep=" ")
