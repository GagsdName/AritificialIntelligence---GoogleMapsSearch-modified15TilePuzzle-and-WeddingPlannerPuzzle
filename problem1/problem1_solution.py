#library for parsing command line arguments
import argparse


city_gps={}
road_segments={}


def is_goal(s, endCityName):
	keys = list(s.keys())
	key = keys[0]
	#print   "\nis goal key", key
	keySplitList = key.split('|')
	if keySplitList[1] == endCityName:
		return True
	
	return False


def successors(dict):
	ret=[]
	path = []
	#print   dict
	parent_key, parent_value = dict.popitem()
	
	parent_item = {parent_key: parent_value}
	print "parent_item", parent_item
	parent_path = parent_item[parent_key]["pathToNode"]
	print "parent_path", parent_path
	parentKeySplitList = parent_key.split('|')
	print "parentKeySplt", parentKeySplitList
	
	#print   "keySplit",keySplitList[1]
	for child_key, child_value in road_segments.iteritems():   # iter on both keys and values
		if child_key.startswith(parentKeySplitList[1]):
			child_item = {child_key:child_value}
			childKeySplitList = child_key.split('|')
			child_item[child_key]["pathToNode"].append(parent_path+childKeySplitList[0])
			child_item[child_key]["costToNode"] = dict[parent_key]["costToNode"] +  child_item[child_key]["distance"]		
			#print   "\nkey:value", key,value
			ret.append({key:value})
		
	print  "\nret", ret
	return ret




def bfs(startCity,endCity,routeOption):
	
	fringe = []
	
	startCityName = str(startCity).strip('[]')
	endCityName = str(endCity).strip('[]')
	#print  startCityName
	
	for key, value in road_segments.iteritems():   # iter on both keys and values
		if key.startswith(startCityName):
			item  = {key:value}
			keySplitList = key.split('|')
			item[key]["pathToNode"].append(startCityName)
			item[key]["pathToNode"].append(keySplitList[1])
			item[key]["costToNode"] = item[key]["distance"]			
			fringe.append(item)
			
	
			
			
	
	#print   fringe
	while len(fringe) > 0:
		#print  "\ninitial fringe\t", fringe
   		for s in successors( fringe.pop(0)):
			#print  "\n\n\nfringe after pop", fringe
			#print  "state", s
			if is_goal(s,endCityName):
				print  "goal", s
				return
			if s not in fringe:
				#print  "nahi"
				fringe.append(s)
				
	return False

	
#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
	
	
	#If routing algorithm is astar
	if "bfs" in routingAlgorithm:
		if "distance" in routingOption:
			bfs(startCity, endCity, routingOption)
			
	
	
	#If routing algorithm is astar
	'''elif "astar" in routingAlgorithm:
		if "distance" in routingOption:
			return#print  "astar"'''
			
				



def get_successor(city):
	return None
	
def readFiles():
	# Parsing the file - 
	with open('city-gps.txt') as fin:
		for line in fin:
			lineSplit = line.split()
			city_gps.update({lineSplit[0]:lineSplit[0], lineSplit[0]+"(latitude)": lineSplit[1], lineSplit[0]+"(longitude)": lineSplit[2]})
			
	# Parsing the file - 
	with open('road-segments.txt') as fin:
		for line in fin:
			lineSplit = line.split()
			#print   lineSplit
			if len(lineSplit) == 5 and int(lineSplit[2]) and int(lineSplit[3]):
				#print   "distance",lineSplit[2],"speed",lineSplit[3]
				road_segments.update({lineSplit[0]+"|"+lineSplit[1]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
					"isHighway":1 if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":[], "costToNode":-1}}); 
			''' TO-DO: handle else case '''
			
	#print   road_segments
	
readFiles()
#parsing command line arguments
cl_parser = argparse.ArgumentParser()
cl_parser.add_argument("startCity", help="Enter the Starting Point of your journey")
cl_parser.add_argument("endCity", help="Enter the Ending Point of your journey")
cl_parser.add_argument("routingOption", help="Enter the Routing Option - One of Segments, Distance, Time or Scenic ")
cl_parser.add_argument("routingAlgorithm", help="Enter the Routing Algorithm - One of bfs, dfs, iterative deepening or astar")
cl_args = cl_parser.parse_args() 
#print  cl_args.startCity
get_driving_directions(cl_args.startCity, cl_args.endCity, cl_args.routingOption, cl_args.routingAlgorithm)


	
	