import random
import platform
import os

game_won = False

board = ['_','_','_','_','_','_','_','_','_',]
locs = {'A1':0, 'A2':3, 'A3':6,'B1':1, 'B2':4, 'B3':7,'C1':2, 'C2':5, 'C3':8}

def SplitUpBoard():
	arr = []
	arr.append(board[:3])	#row1
	arr.append(board[3:6])	#row2
	arr.append(board[6:])	#row3
	arr.append(board[::3])	#col1
	arr.append(board[1::3])	#col2
	arr.append(board[2::3])	#col3
	arr.append(board[::4])	#diag1
	arr.append(board[2:7:2])#diag2
	return arr

def Row1ToGlobal(val):
	return val;
def Row2ToGlobal(val):
	return val + 3;
def Row3ToGlobal(val):
	return val + 6;
def Col1ToGlobal(val):
	return val * 3;
def Col2ToGlobal(val):
	return val * 3+1;
def Col3ToGlobal(val):
	return val * 3+2;
def Diag1ToGlobal(val):
	return val * 4;
def Diag2ToGlobal(val):
	return (val *2) +2;

SectionToGlobals = {	0 : Row1ToGlobal,
			           1 : Row2ToGlobal,
			           2 : Row3ToGlobal,
			           3 : Col1ToGlobal,
			           4 : Col2ToGlobal,
			           5 : Col3ToGlobal,
			           6 : Diag1ToGlobal,
			           7 : Diag2ToGlobal,
}

def PrintBoard(board):
	os.system("cls" if platform.system() == "Windows" else "clear")
	print('  A|B|C\n1|', end='')
	print(board[0] + '|', end='')
	print(board[1] + '|', end='')
	print(board[2] + '|', end='')
	print('\n2|', end='')
	print(board[3] + '|', end='')
	print(board[4] + '|', end='')
	print(board[5] + '|', end='')
	print('\n3|', end='')
	print(board[6] + '|', end='')
	print(board[7] + '|', end='')
	print(board[8] + '|', end='')

	print('')

def MakePlay(loc, val):
	board[locs[loc]] = val

def MakeCompPlay():
	if 'x' in board or 'o' in board:
		if not TryToWin() and not TryToBlock():
			PlaceRandom()
	else:
		first_place = [4,0,2,6,8]
		r = random.randint(0,4)
		board[first_place[r]] = 'o'

def CheckForWin():
	winner = None
	def GetWinner(section):
		x, o = FilledCounter(section[:3])
		if x is 3: return 'Player'
		elif o is 3: return 'Computer'
		elif board.count('_') is 0: return 'Cat'
		else: return None
	
	section_list = SplitUpBoard()
	
	win_responses = []
	win_responses = [GetWinner(item) for item in section_list]

	for item in win_responses:
		if item is 'Player' or item is 'Computer' or item is 'Cat':
			print(str(item), 'wins!!')
			return True

	return False

def PlaceRandom():
	def Randomizer(section):
		x, o = FilledCounter(section)
		if o is 1 and x is 0:
			if section[0] is 'o' and section[2] is '_':\
				return 2
			elif section[2] is 'o' and section[0] is '_':
				return 0
			else:
				r = random.randint(0,10)%2
				while section[r] is not '_':
					r = random.randint(0,10)%2
				return r	
		return -1

	section_list = SplitUpBoard()
	
	possible_randoms_placements = [Randomizer(item) for item in section_list]

	found = False
	for idx, item in enumerate(possible_randoms_placements):
		if item is not -1:
			board[SectionToGlobals[idx](item)] = 'o'
			found = True
			break

	#if there is only one space left
	if not found:
		board[board.index('_')] = 'o'

def TryToWin():	
	section_list = SplitUpBoard()

	exes, ohs = zip(*(FilledCounter(item) for item in section_list))

	for i in range(len(exes)):
		if (exes[i] + ohs[i] < 3) and (ohs[i] == 2):
			board[SectionToGlobals[i](section_list[i].index('_'))] = 'o'
			return True
	return False

def TryToBlock():
	section_list = SplitUpBoard()

	exes,ohs = zip(*(FilledCounter(item) for item in section_list))

	for i in range(len(exes)):
		if (exes[i] + ohs[i] < 3) and (exes[i] == 2):
			board[SectionToGlobals[i](section_list[i].index('_'))] = 'o'
			return True
	return False
	
def FilledCounter(section):
	return section.count('x'), section.count('o')

while game_won is False:
	MakeCompPlay()
	PrintBoard(board)

	if CheckForWin(): break
	
	valid_move = False
	while not valid_move:
		user_play = input('Where would you like to play?\t').upper()

		if user_play in locs.keys():
			if board[locs[user_play]] is '_':
				valid_move = True
			else:
				print('Enter empty space.')
		else:
			print('Enter valid location.')
	
	MakePlay(user_play, 'x')
	
	if CheckForWin(): break