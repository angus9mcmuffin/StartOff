# Proof of concept to find shortest paths between actors given a constructed graph from an adjacency list

import sys

# Derivation of global name to nodes dictionary by assigning the node to its actor's name during creation
def make_nodes(l, d):
	retd = {}
	for name in l:
		actor = Node(name, d[name])
		retd[name] = actor

	return retd

# Used for if you need to put in a premade file that follows as specified: Each new line begins with the first word being the 
# actor's name and all following actors are that actor's friends, all delimited by spaces.
def read_nodes(fn):
	d = {}
	f = open(fn, "r")
	line = f.readline()
	while line != None:
		if line == "":
			break
		actors = line.split()
		if len(actors) == 1:
			d[actors[0]] = []
			continue
		d[actors[0]] = actors[1:]


		line = f.readline()
	f.close()
	ret = {}
	for name in d.keys():
		ret[name] = Node(name, d[name])
	
	return ret
# Quick implementation of the Node object for a graph.
class Node:
	def __init__(self, name, neighbors):
		self._name = name
		self._neighbors = neighbors
	def get_neighbors(self):
		return self._neighbors
	def get_name(self):
		return self._name

# Algorithm to derive shortest path from Node A to Node B given dictionary to translate names to nodes.
def shortpath(A, B, dict_nodes):
	assert type(A) == Node, str(type(A)) + " " + str(A)
	assert type(B) == Node, str(type(B)) + " " + str(B)
	nodes_explored = [A]
	to_explore = []
	def discover(A, B, nodes):
		if A is B:
			nodes.append(B)
			return nodes
		else:
			for neighbor in A.get_neighbors():
				if dict_nodes[neighbor] not in nodes and dict_nodes[neighbor] not in nodes_explored:
					to_explore.append((dict_nodes[neighbor], nodes + [A]))
			if len(to_explore) != 0:
				node_next = to_explore.pop(0)
				return discover(node_next[0], B, node_next[1])
			else:
				return []
	ret = discover(A, B, [])
	retname = []
	for node in ret:
		retname.append(node.get_name())
	return "Path of actors from " + A.get_name() + " to " + B.get_name() + " is: " + str(retname) + " with length " + str(len(ret) - 1) 

def main(argv):
	# Example used to show correctness of solution.
	dict_neighbors = { "Johnny" : ["Carter", "Yselda"], "Carter" : ["Johnny"], "Yselda" : ["Johnny", "Conny"], "Conny" : ["Yselda"]}
	print("Looking at the adj list: " + str(dict_neighbors))
	dict_nodes = make_nodes(dict_neighbors.keys(), dict_neighbors)
	print(shortpath(dict_nodes["Johnny"], dict_nodes["Conny"], dict_nodes))
	# # With -k flag, the script will take the next arguments to be of the format python BFS_actors.py -k file_name actor1 actor2
	# # This will find the shortest path given a file that contains an adjacency list that is delimited with spaces between two actors.
	# if "-k" in argv:
	# 	print("Reading Nodes from " + str(argv[2]))
	# 	dict_nodes = read_nodes(argv[2])

	# 	print(shortpath(dict_nodes[argv[3]], dict_nodes[argv[4]], dict_nodes))
	
	# # This was written to see if correct solutions were given for any given name included in the list of names in dict_neighbors
	# if len(argv) == 3:
	# 	print(shortpath(dict_nodes[argv[1]], dict_nodes[argv[2]], dict_nodes)) 


if __name__ == "__main__":
	main(sys.argv)


# This example code is to provide proof of concept that we discussed in the interview. 
# The changes made that were not covered in the interview were details involving how to track names to nodes and edge cases to ensure no cycles. 

