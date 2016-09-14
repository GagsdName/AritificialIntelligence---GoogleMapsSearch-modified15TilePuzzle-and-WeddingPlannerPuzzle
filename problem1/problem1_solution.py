#library for parsing command line arguments
import argparse

#function to suggest good driving directions 
def get_driving_directions(startCity,endCity,routingOption,routingAlgorithm):
	'''
	'''

#parsing command line arguments
cl_parser = argparse.ArgumentParser()
cl_parser.add_argument("startCity", help="Enter the Starting Point of your journey")
cl_parser.add_argument("endCity", help="Enter the Ending Point of your journey")
cl_parser.add_argument("routingOption", help="Enter the Routing Option ")
cl_parser.add_argument("routingAlgorithm", help="Enter the Routing Algorithm - 1) bfs 2)dfs 3)iterative deepening 4)astar")
cl_args = cl_parser.parse_args() 

get_driving_directions(cl_args.startCity, cl_args.endCity, cl_args.routingOption, cl_args.routingAlgorithm)

# Parsing the file - 
'''with open('city-gps.txt') as fin:
	for line in fin:
		#print "\t".join(line.split()) + "\n"
	'''	
	
	