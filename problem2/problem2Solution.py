# https://pythonandr.com/2015/07/20/number-of-inversions-in-an-unsorted-array-python-code/
import sys

state = []
goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
count = 0
input_file = open(sys.argv[1],'r')
for line in input_file:
	row = line.split(' ')
	row = map(lambda s:s.strip(), row)
	state.append([int(i) for i in row])
	
#print puzzle board	
def print_state1(state):
    for row in state:
        print row,"\n"
        
#swap empty tile with given tile        
def swap(state,row,col,nrow,ncol):
    temp=state[row][col]
    state[row][col]=state[nrow][ncol]
    state[nrow][ncol]=temp
    return state
    
#generate successors of the given state
def successors(state):
    suc=[]
    for row in range(0,4):
        for col in range(0,4):
            if int(state[row][col])==0:
                emp_row=row
                emp_col=col
    left_succ=swap(state,emp_row,emp_col,emp_row,emp_col-1 if emp_col else 3)
    right_succ=swap(state,emp_row,emp_col,emp_row,emp_col+1 if emp_col<3 else 0)
    up_succ=swap(state,emp_row,emp_col,emp_row-1 if emp_row else 3,emp_col)
    down_succ=swap(state,emp_row,emp_col,emp_row+1 if emp_col<3 else 0,emp_col)
    suc.append(left_succ)
    suc.append(right_succ)
    uc.append(up_succ)
    suc.append(down_succ)
    return suc	

#print state in a human readable format
def print_state(state):
	for row in state:
		for n in row:
			print str(n).rjust(2),
		print

#heuristic function, uses manhattan distance
#calculates the manhattan distance between a given n and its goal-state position
def heuristic(state, n):
	zposg, zposc = 0, 0
	#find n in current state
	for i,row in enumerate(state):
		for j,no in enumerate(row):
			if no == n:
				zposc = i,j
	
	#find n in goal state
	for i,row in enumerate(goal_state):
		for j,no in enumerate(row):
			if no == n:
				zposg = i,j
	
	return (abs(zposc[0] - zposg[0]) + abs(zposc[1] - zposg[1])), zposc, zposg

#recursively count the number of inversions in a list
def count_inversions(l):
	global count
	midsection = len(l)/2
	leftArray = l[:midsection]
	rightArray = l[midsection:]
	if len(l) > 1:
		count_inversions(leftArray)
		count_inversions(rightArray)
		i, j = 0, 0
		a = leftArray; b = rightArray
		for k in range(len(a) + len(b) + 1):
			if a[i] <= b[j]:
				l[k] = a[i]
				i += 1
				if i == len(a) and j != len(b):
					while j != len(b):
						k +=1
						l[k] = b[j]
						j += 1
					break
			elif a[i] > b[j]:
				l[k] = b[j]
				count += (len(a) - i)
				j += 1
				if j == len(b) and i != len(a):
					while i != len(a):
						k+= 1
						l[k] = a[i]
						i += 1
					break
	return l

#count the number of inversions in the given state
def inversions(state):
	#find position of zero
	global count
	zpos = 0
	for i,row in enumerate(state):
		for j,n in enumerate(row):
			if n == 0:
				zpos = i,j
	l = []
	# count inversions normally
	for row in state:
		for n in row:
			l.append(n)
	count_inversions(l)
	# subtract the inversion from zero count from total
	return (count - (zpos[0]*4 + zpos[1]))
	count = 0

#solve 15 puzzle problem
print inversions(state)
for row in state:
	for n in row:
		print heuristic(state, n)
print inversions(goal_state)
