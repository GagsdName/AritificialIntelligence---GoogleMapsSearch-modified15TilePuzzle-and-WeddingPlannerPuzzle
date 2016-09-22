# https://pythonandr.com/2015/07/20/number-of-inversions-in-an-unsorted-array-python-code/
import sys
import heapq

state = [[15,2,3,4],[5,6,7,8],[12,10,11,9],[13,14,1,0]]
goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
count = 0
pq = []
#input_file = open(sys.argv[1],'r')
#for line in input_file:
#	row = line.split(' ')
#	row = map(lambda s:s.strip(), row)
#	state.append([int(i) for i in row])
	

        
#swap empty tile with given tile        
def swap(state,row,col,nrow,ncol):
    temp_state=copy.deepcopy(state)
    print temp_state
    temp=temp_state[row][col]
    temp_state[row][col]=temp_state[nrow][ncol]
    temp_state[nrow][ncol]=temp
    return temp_state
    
#generate successors of the given state
def successors(state):
    suc=[]
    for row in range(0,4):
        for col in range(0,4):
            if int(state[row][col])==0:
                emp_row=row
                emp_col=col
    right_succ=swap(state,emp_row,emp_col,emp_row,emp_col-1 if emp_col else 3)
    left_succ=swap(state,emp_row,emp_col,emp_row,emp_col+1 if emp_col<3 else 0)
    down_succ=swap(state,emp_row,emp_col,emp_row-1 if emp_row else 3,emp_col)
    up_succ=swap(state,emp_row,emp_col,emp_row+1 if emp_row<3 else 0,emp_col)
    suc.append(right_succ)
    suc.append(left_succ)
    suc.append(down_succ)
    suc.append(up_succ)
    return suc
    

#print state in a human readable format
def print_state(state):
	for row in state:
		for n in row:
			print str(n).rjust(2),
		print

#heuristic function, uses manhattan distance
#calculates the manhattan distance between a given tile number n and its position in the goal-state
def heuristic_n(state, n):
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

#calculates the manhattan distance between a given state and goal
def heuristic(state):
        cost = 0
        for i in range(0,16):
            cost += heuristic_n(state,n)
        return cost

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



#a-star search algorithm
def a_star(state):
    state_tuple = (0,0,state,"")
    heapq.heappush(pq,state_tuple)
    while not pq.empty():
        cost, state, path = heapq.heappop(pq)
        for s in successors(state):
            heapq.heappush(pq,(1+state))
    

#solve 15 puzzle problem
print inversions(state)
#for row in state:
#	for n in row:
#		print heuristic(state, n)
heuristic(state)
print inversions(goal_state)
