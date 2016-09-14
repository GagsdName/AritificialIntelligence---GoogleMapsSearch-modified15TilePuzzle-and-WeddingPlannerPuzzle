#library for parsing command line arguments
import argparse
city_gps=[]
road_segments=[]

#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
	if "astar" in routingAlgorithm:
		if "distance" in routingOption:
			print "hai"

			
def get_successor(city):
	successor = []
	return successor
	
def readFiles():
	city_gps_entry =[]
	road_segments_entry=[]
	
	# Parsing the file - 
	with open('city-gps.txt') as fin:
		for line in fin:
			city_gps.append(line.split())
			
	# Parsing the file - 
	with open('road-segments.txt') as fin:
		for line in fin:
			road_segments.append(line.split())

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


	
	