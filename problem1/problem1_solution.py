#library for parsing command line arguments
import argparse


city_gps={}
road_segments={}


def is_goal(s, endCityName):
	key, value = s.popitem()
	keySplitList = key.split('|')
	if keySplitList[1] == endCityName:
		return True
	
	return False


def successors(dict):
	ret=[]
	key, value = dict.popitem()
	keySplitList = key.split('|')
	
	for key, value in road_segments.iteritems():   # iter on both keys and values
		if key.startswith(keySplitList[1]):
			ret.append({key:value})
		
	
	return ret




def bfs(startCity,endCity):
	
	fringe = []
	startCityName = str(startCity).strip('[]')
	endCityName = str(endCity).strip('[]')
	#print startCityName
	
	for key, value in road_segments.iteritems():   # iter on both keys and values
		if key.startswith(startCityName):
			fringe.append({key:value})
	
	#print fringe
	while len(fringe) > 0:
   		for s in successors( fringe.pop(0)):
			if is_goal(s,endCityName):
				print s
			if s not in fringe:
				fringe.append(s)
				
	return False

	
#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
	
	#If routing algorithm is astar
	if "bfs" in routingAlgorithm:
		if "distance" in routingOption:
			bfs(startCity, endCity)
			
	
	
	#If routing algorithm is astar
	elif "astar" in routingAlgorithm:
		if "distance" in routingOption:
			print "astar"
			
				

			
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
			#print lineSplit
			if len(lineSplit) == 5 and int(lineSplit[2]) and int(lineSplit[3]):
				#print "distance",lineSplit[2],"speed",lineSplit[3]
				road_segments.update({lineSplit[0]+"|"+lineSplit[1]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
					"isHighway":1 if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3])}}); 
			''' TO-DO: handle else case '''
			
	#print road_segments
	
readFiles()
#parsing command line arguments
cl_parser = argparse.ArgumentParser()
cl_parser.add_argument("startCity", help="Enter the Starting Point of your journey")
cl_parser.add_argument("endCity", help="Enter the Ending Point of your journey")
cl_parser.add_argument("routingOption", help="Enter the Routing Option - One of Segments, Distance, Time or Scenic ")
cl_parser.add_argument("routingAlgorithm", help="Enter the Routing Algorithm - One of bfs, dfs, iterative deepening or astar")
cl_args = cl_parser.parse_args() 

get_driving_directions(cl_args.startCity, cl_args.endCity, cl_args.routingOption, cl_args.routingAlgorithm)


	
	