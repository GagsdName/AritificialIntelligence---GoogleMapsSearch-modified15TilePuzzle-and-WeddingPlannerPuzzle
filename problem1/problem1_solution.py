#library for parsing command line arguments
import argparse
city_gps={}
road_segments={}

#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
	#If routing algorithm is astar
	if "astar" in routingAlgorithm:
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
			if len(lineSplit) == 5:
				road_segments.update({lineSplit[0]+"(source)":lineSplit[0], lineSplit[0]+"(destination)": lineSplit[1],\
				lineSplit[0]+"(length)": lineSplit[2], lineSplit[0]+"(speed-limit)": lineSplit[3], lineSplit[0]+"(highway)": lineSplit[4]})
			''' TO-DO: handle else case '''
			
	#print city_gps
	
readFiles()
#parsing command line arguments
cl_parser = argparse.ArgumentParser()
cl_parser.add_argument("startCity", help="Enter the Starting Point of your journey")
cl_parser.add_argument("endCity", help="Enter the Ending Point of your journey")
cl_parser.add_argument("routingOption", help="Enter the Routing Option - One of Segments, Distance, Time or Scenic ")
cl_parser.add_argument("routingAlgorithm", help="Enter the Routing Algorithm - One of bfs, dfs, iterative deepening or astar")
cl_args = cl_parser.parse_args() 

get_driving_directions(cl_args.startCity, cl_args.endCity, cl_args.routingOption, cl_args.routingAlgorithm)


	
	