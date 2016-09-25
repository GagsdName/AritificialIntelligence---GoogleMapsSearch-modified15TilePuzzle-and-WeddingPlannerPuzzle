#library for getting command line arguments
import sys
import heapq
from math import sin, cos, sqrt, atan2, radians

city_gps={} #city gps dictionary with parsed entries from city_gps file
road_segments={} #road_segments dictionary with parsed entries from road_segments file
goal_cost = 9999999999 #goal_cost initialized to an arbitrary high value
goal_path = "" #path to goal initialized
goal_time = 0.0 #goal time initialized to 0 
goal_dist = 0.0 #goal  distance to initialized to 0 
goal_flag =0 #goal flag initialized to 0 

'''finding a neighbor closest to goal when the extracted node is a highway intersection and therefore no corresponding entry is found in the city_gps file
The neighbor is chosen on the basis that it has the least value for the applied heuristic'''
def find_neighbor_closest_to_goal(highwayIntersection, fromCity):
        
        min_heuristic = 9999999999 #minimum heuristic initialized to an arbitarly high value
	min_neighbor = {} #the neighbor to be returned is initialized to an empty dictionary
	minKey="" #the key string for the minimum neighbor entry	
    	for child_key, child_value in road_segments.iteritems():
		childKeySplitList = key_split(child_key)
		if childKeySplitList[0] == highwayIntersection and childKeySplitList[1] != fromCity :
                	child_item = {child_key:child_value}
			euc_distance = calc_heuristic(childKeySplitList[1], endCityName)
			if euc_distance != None:
				heuristic = float(child_item[child_key]["distance"])+euc_distance
				if heuristic < min_heuristic:
					min_heuristic = heuristic
					min_neighbor = child_item
					minKey = child_key
        minKeySplitList = minKey.split("|")						
	return (min_heuristic, min_neighbor, minKey, minKeySplitList[1])
'''
Function to calculate heuristic for any city. The straighline distance calculation from source - http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude-python  	
'''
def calc_heuristic(src, dest):
	if src not in list(city_gps.keys()):
		 print "\nNo entry in City_Gps file for\t", src, "\n"	
		 return None
	#print "\nlatitude src = ", city_gps[src]["latitude"]
	distance = 0
	if routeOptionString == "distance":
		# approximate radius of earth in km
		R = 6373.0 * 0.621371
		lat1 = city_gps[src]["latitude"]
		lon1 = city_gps[src]["longitude"]
		lat2 = city_gps[dest]["latitude"]
		lon2 = city_gps[dest]["longitude"]
		
		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c
		
	return distance
'''
Function that implements astar
'''
def astar():
	fringe = [] #initializing an empty fringe - implemented as a priority queue
	global goal_cost
	global goal_path
        global goal_time
        global goal_dist
	# iter on both keys and values
    	for key, value in road_segments.iteritems():
		key_tokens = key_split(key)
		if key_tokens[0] == startCityName:
			item  = {key:value}
			item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName #updating path of the node being explored
			item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
			item[key]["timeToNode"] = item[key]["travelTime"] #updating travel time of the node being explored
                        item[key]["distToNode"] = float(item[key]["distance"]) # distance to the node being explored
                        item[key]["costToNode"] = item[key][routeOptionString] # cost to node - the routing Option entry updated for the node being explored
			g = calc_heuristic(key_tokens[1], endCityName) #calculate heuristic function called
			if g != None: # if a latitude longitude entry is found for the node being explored
				f = float(item[key]["costToNode"]) + g
                                heapq.heappush(fringe, (f,item)) #pushing in the fringe
			else:#if no latitude longitude entry is found for the node being  explored - meaning it is a highway intersection
				highway_neighbor_tuple = find_neighbor_closest_to_goal(key_tokens[1], key_tokens[0])
				print "\nhighway neighbor tuple entry",highway_neighbor_tuple[1]
				if highway_neighbor_tuple != None:#if the neighbor of the highway intersection is not another highway intersection
					'''Updating entries for the neighbor entry found for the highway intersection'''
					road_segments[highway_neighbor_tuple[2]]["pathToNode"] = item[key]["pathToNode"]+"|"+highway_neighbor_tuple[3]
					road_segments[highway_neighbor_tuple[2]]["costToNode"] = float(item[key]["costToNode"])+float(highway_neighbor_tuple[0])
					road_segments[highway_neighbor_tuple[2]]["distToNode"] = float(item[key]["distToNode"])+\
						float( road_segments[highway_neighbor_tuple[2]]["distance"])
					#pushing into the fringe
					heapq.heappush(fringe,(road_segments[highway_neighbor_tuple[2]]["costToNode"], highway_neighbor_tuple[1]))
					
        ''' poppping from the fringe the entry with the least value of function f(s) = sum of path to node and heuristic to goal,
         and checking if the goal is reached'''	
	while len(fringe) > 0:
		popped_item = heapq.heappop(fringe)[1]
		for s in successors(popped_item):
			keys = list(s.keys())
                        s_key = keys[0]
			if is_goal(s,endCityName):
                		float_val = float(s[s_key]["costToNode"])
                		if float_val < goal_cost:
                        		goal_cost = float(s[s_key]["costToNode"])
                        		goal_path = s[s_key]["pathToNode"]
                        		goal_time = float(s[s_key]["timeToNode"])
                        		goal_dist = float(s[s_key]["distToNode"])
                       	 		continue
            		if s not in fringe: #if the successor is not a goal and not a state which has already been added to the fringe, add it to the fringe
                		heapq.heappush(fringe,(s[s_key]["costToNode"],s))
	return None

'''
Function that splits a key string(in the format - "startCity|EndCity|HighwayName")
'''
def key_split(key):
    keySplitList = key.split('|')
    return keySplitList

'''
Function that checks if the goal is reached.
'''    
def is_goal(s, endCityName):
    keys = list(s.keys())
    key = keys[0]
    keySplitList = key.split('|')
    '''Checking to see if the node is a goal node '''
    if keySplitList[1] == endCityName:
        s[key]["pathToNode"] = s[key]["pathToNode"] + "|"+endCityName
        return True
    
    return False

'''
Function to calculate successors of a given city - or neighbors of that city - or cities reachable from a particular city 
'''
def successors(dict):
    
    global goal_path
    global goal_cost
    global goal_dist
    global goal_time
    #Checking to see if the argument passed to this function is itself not a goal
    if is_goal(dict,endCityName):
    	keys = list(dict.keys())
        s_key = keys[0]
        float_val = float(dict[s_key]["costToNode"])
	#updating global variables if the it is indeed a goal state
        if float_val < goal_cost:
        	goal_cost = float(dict[s_key]["costToNode"])
                goal_path = dict[s_key]["pathToNode"]
		goal_time = float(dict[s_key]["timeToNode"])
		goal_dist = float(dict[s_key]["distToNode"])
                
    ret=[]
    path = []
    keys = list(dict.keys())
    ''' extracting key and value details of the node whose successors are to b generated '''
    parent_key = keys[0]
    parent_value = dict[parent_key]
    parent_item = {parent_key: parent_value}
    parent_path= parent_item[parent_key]["pathToNode"]
    parentKeySplitList = parent_key.split('|')
    pathList = parent_path.split('|')
    #finding successors now 
    for child_key, child_value in road_segments.iteritems():
        childKeySplitList = key_split(child_key)
        if childKeySplitList[0] == parentKeySplitList[1] and childKeySplitList[1] not in pathList:
            	child_item = {child_key:child_value}
            	child_item[child_key]["pathToNode"] = parent_path+ "|"+childKeySplitList[1]
            	child_item[child_key]["costToNode"] = float(dict[parent_key]["costToNode"]) +  float(child_item[child_key][routeOptionString]) 
		child_item[child_key]["distToNode"] = float(dict[parent_key]["distToNode"]) +  float(child_item[child_key]["distance"])
		child_item[child_key]["timeToNode"] = float(dict[parent_key]["timeToNode"]) +  float(child_item[child_key]["travelTime"])	
		#checking against normal costToNode values in case of bfs, dfs and idfs
		if "bfs" in routingAlgorithm or "dfs" in routingAlgorithm or "idfs" in routingAlgorithm:
			if(child_item[child_key]["costToNode"]< goal_cost): 
        #if it does not have a value greater than the minimum goal cost so far it is added to the list being returned
				ret.append({child_key:child_value})
		elif "astar" in routingAlgorithm: #checking against f(s) values for nodes in case of astar
			latLongDistance = calc_heuristic(childKeySplitList[0],endCityName)
			if latLongDistance != None:
				heuristic = child_item[child_key]["costToNode"] + latLongDistance
			else:
				heuristic = child_item[child_key]["costToNode"]  
			if heuristic < goal_cost: 
	#if the calculate heuristic function is less than the goal cost minimum so far, the node is added to the list being returned 
				child_item[child_key]["costToNode"] = heuristic
				ret.append({child_key:child_value})
					
    return ret
'''
Function to implement Depth First Search
'''
def dfs():
    
    fringe = []
    global goal_cost
    global goal_path
    global goal_time
    global goal_dist
    global goal_flag
#Initializing the fringe with the first level of successors of the startCity
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
            item[key]["timeToNode"] = item[key]["travelTime"]
            item[key]["distToNode"] = item[key]["distance"]
            item[key]["costToNode"] = item[key][routeOptionString]
  
            fringe.append(item)
	curr_depth=1
	#Extracting from the fringe, finding successors and checking against the goal cost for a minimum #	
    while len(fringe)>0:
        for s in successors(fringe.pop()):
            if is_goal(s,endCityName):
		keys = list(s.keys())
		s_key = keys[0]
		float_val = float(s[s_key]["costToNode"])
		if float_val < goal_cost:
			goal_cost = float(s[s_key]["costToNode"])
			goal_path = s[s_key]["pathToNode"]
			goal_time = float(s[s_key]["timeToNode"])
			goal_dist = float(s[s_key]["distToNode"])
                        continue
		curr_depth+=1
            if s not in fringe:
                fringe.append(s)
    goal_flag=1   
                
    return False
'''
Function to implement Iterative Depth First Search. Levereges DFS iteratively 
'''
def idfs():
    global goal_flag
    depth=0
    while(not goal_flag):
        dfs(depth+1)
    
'''
Function to implement Breadth First Search
'''	
def bfs():
    
    fringe = []
    global goal_cost
    global goal_path
    global goal_dist
    global goal_time

    ''' Initializing the fringe with the first level of successors of the startCity'''
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
	    item[key]["timeToNode"] = item[key]["travelTime"]
	    item[key]["distToNode"] = item[key]["distance"]    
            item[key]["costToNode"] = item[key][routeOptionString]	    
	    fringe.append(item)
 #Extracting from the fringe, finding successors and checking against the goal cost for a minimum #
    while len(fringe) > 0:
           for s in successors( fringe.pop(0)):
            if is_goal(s,endCityName):
		keys = list(s.keys())
		s_key = keys[0]
		float_val = float(s[s_key]["costToNode"])
		if float_val < goal_cost:
			goal_cost = float(s[s_key]["costToNode"])
			goal_path = s[s_key]["pathToNode"]
			goal_time = float(s[s_key]["timeToNode"])
			goal_dist = float(s[s_key]["distToNode"])
		continue
            
            
            if s not in fringe:
                fringe.append(s)
                
    return False

'''
Function that calls different search functions based on input parameters
'''
    
#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
    
    global startCityName, endCityName, routeOptionString, routingAlgoString
    #forming strings corresponding to input command line arguments 
    startCityName = str(startCity).strip('[]')
    endCityName = str(endCity).strip('[]')
    routeOptionString = str(routingOption).strip('[]')
    routingAlgoString = str(routingAlgorithm).strip('[]')
    ''' Calling appropriate functions '''         
    if "bfs" in routingAlgorithm:
            bfs()
    if "dfs" in routingAlgorithm:
            dfs()
    if "ids" in routingAlgorithm:
            ids()
    if "astar" in routingAlgorithm:
            astar()
            
'''
Function to read and parse input files into dictionaries
'''    
def readFiles():
    # Parsing the file - 
    with open('city-gps.txt') as fin:
        for line in fin:
            lineSplit = line.split()
            city_gps.update({lineSplit[0]:{"latitude": float(lineSplit[1]), "longitude": float(lineSplit[2])}})
	#print city_gps
            
    # Parsing the file - 
    with open('road-segments.txt') as fin:
        for line in fin:
            lineSplit = line.split()
            if len(lineSplit) == 5 and int(lineSplit[2]) and int(lineSplit[3]):
                road_segments.update({lineSplit[0]+"|"+lineSplit[1]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
                    "scenic":lineSplit[2] if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":"", "costToNode":0,\
			"timeToNode" : 0.0,"distToNode":0.0, "segments":1}}); 
                road_segments.update({lineSplit[1]+"|"+lineSplit[0]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
                    "scenic":lineSplit[2] if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":"", "costToNode":0,
			"timeToNode":0.0, "distToNode":0.0, "segments":1}});
            
#read Text Files     
readFiles()
#Reac program run arguments
startCity=sys.argv[1]
endCity=sys.argv[2]
routingOption=sys.argv[3]
routingAlgorithm=sys.argv[4]
if startCity != endCity:
	get_driving_directions(startCity,endCity,routingOption,routingAlgorithm)
	print "\nLatLong Distance between Source and Destination is - ",calc_heuristic(startCityName, endCityName), "miles\n"
	print "\n[total-distance-in-miles:", goal_dist, "] [total-time-in-hours:", goal_time,"] ", goal_path
else: 
	print "\nStart City and End City are same ! Re-run the program with different set of arguments\n"


    
    
