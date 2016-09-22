#parsing input
import sys

#list of tuples containing set of friendships
friends = []
#set containing all the guests present
guests = set()
#total number of guests
no_of_guests = len(guests)
#dictionary contains a guest name and a set of people unknown to guest
unknown_to_guest = { guest: get_unknown(guest) for guest in guests }
#set containing arranged people
sel_guests = set()
#list containing arrangement of tables
tables = []

input_file = open(sys.argv[1],'r')
seats_per_table = int(sys.argv[2])
for line in input_file:
	friend_list = line.split(' ')
	friend_list = map(lambda s: s.strip(), friend_list)
	guest = friend_list.pop(0)
	guests.add(guest)
	for f in friend_list:
		friends.append((guest,f))
		guests.add(f)

#return a set of people unknown to a particular guest
def get_unknown(guest):
	ug = set(guests)
	for guest1,guest2 in friends:
		if guest in (guest1,guest2):
			ug.discard(guest1)
			ug.discard(guest2)
	return ug

#returns true if the guest can be added to the table
def addable_guest(table,guest):
	if guest in sel_guests:
		return False
	elif len(table) == 0:
		return True
	else:
		aml = unknown_to_guest[table[0]]
		for member in table:
			aml &= unknown_to_guest[member]
		if guest in aml:
			return True
		else:
			return False

#print "Start arrangement"
while len(tables) < no_of_guests:
	table = []
	if len(sel_guests) >= len(guests):
		break
	for guest in guests:
		if addable_guest(table,guest) and len(table) < seats_per_table and len(sel_guests) < len(guests):
			table.append(guest)
			sel_guests.add(guest)
	tables.append(table)

#print solution
print len(tables),
for table in tables:
	for member in table:
		print member + ',',
	print ' ',
