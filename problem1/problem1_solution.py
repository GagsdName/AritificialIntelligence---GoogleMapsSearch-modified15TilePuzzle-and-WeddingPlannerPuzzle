#library for getting command line arguments
import sys
#from geopy.distance import vincenty

city_gps={}
road_segments={}
'''
def calc_heuristic(src, dest):
	src1 = (src["latitude"], src["longitude"])
	dest1 = (dest["latitude"], dest["longitude"])
	return(vincenty(src1, dest1).miles)

def astar():
	fringe = []
	global goal_cost
    global goal_path
    goal_path=""
    goal_cost=9999999999
    
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
            item[key]["costToNode"] = item[key][routeOptionString]    
            fringe.append(item)

    while len(fringe) > 0:
           for s in successors( fringe.pop(0)):
            if is_goal(s,endCityName):
                keys = list(s.keys())
                s_key = keys[0]
                float_val = float(s[s_key]["costToNode"])
                if float_val < goal_cost:
                    goal_cost = float(s[s_key]["costToNode"])
                    goal_path = s[s_key]["pathToNode"]
                    continue
            
            
            if s not in fringe:
                fringe.append(s)
                
	return None
'''
def key_split(key):
    keySplitList = key.split('|')
    return keySplitList
    
def is_goal(s, endCityName):
    keys = list(s.keys())
    key = keys[0]
    keySplitList = key.split('|')
    if keySplitList[1] == endCityName:
        s[key]["pathToNode"] = s[key]["pathToNode"] + "|"+endCityName
        return True
    
    return False


def successors(dict):
    ret=[]
    path = []
    keys = list(dict.keys())
    parent_key = keys[0]
    parent_value = dict[parent_key]
    parent_item = {parent_key: parent_value}
    parent_path= parent_item[parent_key]["pathToNode"]
    parentKeySplitList = parent_key.split('|')
    pathList = parent_path.split('|')
    for child_key, child_value in road_segments.iteritems():
        childKeySplitList = key_split(child_key)
        if childKeySplitList[0] == parentKeySplitList[1] and childKeySplitList[1] not in pathList:
            child_item = {child_key:child_value}
            child_item[child_key]["pathToNode"] = parent_path+ "|"+childKeySplitList[1]
            child_item[child_key]["costToNode"] = float(dict[parent_key]["costToNode"]) +  float(child_item[child_key][routeOptionString]) 
            if(child_item[child_key]["costToNode"]<= goal_cost):
                ret.append({child_key:child_value})
    return ret

	
def dfs():
    
    fringe = []
    global goal_cost
    global goal_path
    goal_path=""
    goal_cost=9999999999
    
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
            item[key]["costToNode"] = item[key][routeOptionString]    
            fringe.append(item)
    #count=0
    while len(fringe)>0:
       # pop_item=fringe.pop(count)
        for s in successors(fringe.pop()):
            #scount=successors(pop_item)
            #count=count+len(scount)
            if is_goal(s,endCityName):
                #print "goal",s
                keys = list(s.keys())
                s_key = keys[0]
                float_val = float(s[s_key]["costToNode"])
                if float_val < goal_cost:
                    goal_cost = float(s[s_key]["costToNode"])
                    goal_path = s[s_key]["pathToNode"]
                    continue
            if s not in fringe:
                fringe.append(s)
           
                
    return False
	
def bfs():
    
    fringe = []
    global goal_cost
    global goal_path
    goal_path=""
    goal_cost=9999999999
    
    for key, value in road_segments.iteritems():   # iter on both keys and values
        key_tokens = key_split(key)
        if key_tokens[0] == startCityName:
            item  = {key:value}
            item[key]["pathToNode"] = item[key]["pathToNode"] + "|"+startCityName
            item[key]["pathToNode"] = item[key]["pathToNode"]+"|"+key_tokens[1]
            item[key]["costToNode"] = item[key][routeOptionString]    
            fringe.append(item)

    while len(fringe) > 0:
           for s in successors( fringe.pop(0)):
            if is_goal(s,endCityName):
                keys = list(s.keys())
                s_key = keys[0]
                float_val = float(s[s_key]["costToNode"])
                if float_val < goal_cost:
                    goal_cost = float(s[s_key]["costToNode"])
                    goal_path = s[s_key]["pathToNode"]
                    continue
            
            
            if s not in fringe:
                fringe.append(s)
                
    return False

    
#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
    
    global startCityName, endCityName, routeOptionString
    startCityName = str(startCity).strip('[]')
    endCityName = str(endCity).strip('[]')
    routeOptionString = str(routingOption).strip('[]')
    if "bfs" in routingAlgorithm:
            bfs()
    if "dfs" in routingAlgorithm:
            dfs()
    if "ids" in routingAlgorithm:
             ids()
#     if "astar" in routingAlgorithm:
#             astar()
            
def get_successor(city):
    return None
    
def readFiles():
    # Parsing the file - 
    with open('city-gps.txt') as fin:
        for line in fin:
            lineSplit = line.split()
            city_gps.update({lineSplit[0]:{"latitude": lineSplit[1], "longitude": lineSplit[2]}})
	#print city_gps
            
    # Parsing the file - 
    with open('road-segments.txt') as fin:
        for line in fin:
            lineSplit = line.split()
            if len(lineSplit) == 5 and int(lineSplit[2]) and int(lineSplit[3]):
                road_segments.update({lineSplit[0]+"|"+lineSplit[1]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
                    "isHighway":1 if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":"", "costToNode":0}}); 
                road_segments.update({lineSplit[1]+"|"+lineSplit[0]+"|"+lineSplit[4]:{"distance": lineSplit[2], "speed": lineSplit[3],\
                    "isHighway":1 if lineSplit[3] >=55 else 0, "travelTime": float(lineSplit[2])/float(lineSplit[3]), "pathToNode":"", "costToNode":0}});
            
    
readFiles()

startCity=sys.argv[1]
endCity=sys.argv[2]
routingOption=sys.argv[3]
routingAlgorithm=sys.argv[4]

get_driving_directions(startCity,endCity,routingOption,routingAlgorithm)
print "\npath:",goal_path," \ncost:",goal_cost



    
    
