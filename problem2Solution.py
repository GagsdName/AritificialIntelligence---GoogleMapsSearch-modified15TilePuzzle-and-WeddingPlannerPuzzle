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

#print state in a human readable format
def print_state(state):
	for row in state:
		for n in row:
			print str(n).rjust(2),
		print

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
	print count - (zpos[0]*4 + zpos[1])
	count = 0

#solve 15 puzzle problem
inversions(state)
inversions(goal_state)

