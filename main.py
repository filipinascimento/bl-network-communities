#!/usr/bin/env python

import sys
import os.path
import re
import json
import numpy as np
from tqdm import tqdm
import igraph as ig
import louvain
# import infomap


def louvain_find_partition_multiplex(graphs, partition_type,layer_weights=None, seed=None, **kwargs):
	""" Detect communities for multiplex graphs.
	Each graph should be defined on the same set of vertices, only the edges may
	differ for different graphs. See
	:func:`Optimiser.optimise_partition_multiplex` for a more detailed
	explanation.
	Parameters
	----------
	graphs : list of :class:`ig.Graph`
		List of :class:`louvain.VertexPartition` layers to optimise.
	partition_type : type of :class:`MutableVertexPartition`
		The type of partition to use for optimisation (identical for all graphs).
	seed : int
		Seed for the random number generator. By default uses a random seed
		if nothing is specified.
	**kwargs
		Remaining keyword arguments, passed on to constructor of ``partition_type``.
	Returns
	-------
	list of int
		membership of nodes.
	float
		Improvement in quality of combined partitions, see
		:func:`Optimiser.optimise_partition_multiplex`.
	Notes
	-----
	We don't return a partition in this case because a partition is always
	defined on a single graph. We therefore simply return the membership (which
	is the same for all layers).
	See Also
	--------
	:func:`Optimiser.optimise_partition_multiplex`
	:func:`slices_to_layers`
	Examples
	--------
	>>> n = 100
	>>> G_1 = ig.Graph.Lattice([n], 1)
	>>> G_2 = ig.Graph.Lattice([n], 1)
	>>> membership, improvement = louvain.find_partition_multiplex([G_1, G_2],
	...                                                            louvain.ModularityVertexPartition)
	"""
	n_layers = len(graphs)
	partitions = []
	if(layer_weights is None):
		layer_weights = [1]*n_layers
	for graph in graphs:
		partitions.append(partition_type(graph, **kwargs))
	optimiser = louvain.Optimiser()

	if (not seed is None):
		optimiser.set_rng_seed(seed)

	improvement = optimiser.optimise_partition_multiplex(partitions, layer_weights)
	return partitions[0].membership, improvement


def check_symmetric(a, rtol=1e-05, atol=1e-08):
	return np.allclose(a, a.T, rtol=rtol, atol=atol)

def isFloat(value):
	if(value is None):
		return False
	try:
		numericValue = float(value)
		return np.isfinite(numericValue)
	except ValueError:
		return False

def loadCSVMatrix(filename):
	return np.loadtxt(filename,delimiter=",")






# def infomapMembership(g, parameters):
# 	vertexCount = g.vcount()
# 	infomapSimple = infomap.Infomap(parameters)
# 	infomapSimple.setVerbosity(0)
# 	infoNetwork = infomapSimple.network()
# 	for nodeIndex in range(0,vertexCount):
# 		infoNetwork.addNode(nodeIndex)
# 	weighted = "weights" in g.edge_attributes()
# 	for edge in edges:
# 		weight = 1.0
# 		if(weighted):
# 			weight = edge["weight"];
# 		infoNetwork.addLink(edge.source, edge.target)

# 	infomapSimple.run()
# 	membership = [0]*vertexCount
# 	# print("Result")
# 	# print("\n#node module")
# 	for node in infomapSimple.iterTree():
# 		if node.isLeaf():
# 			# print((node.physicalId,node.moduleIndex()));
# 			membership[node.physicalId] = node.moduleIndex();
# 	return membership;

configFilename = "config.json"
argCount = len(sys.argv)
if(argCount > 1):
		configFilename = sys.argv[1]

outputDirectory = "output"
csvOutputDirectory = os.path.join(outputDirectory, "csv")

if(not os.path.exists(outputDirectory)):
		os.makedirs(outputDirectory)

if(not os.path.exists(csvOutputDirectory)):
		os.makedirs(csvOutputDirectory)

with open(configFilename, "r") as fd:
		config = json.load(fd)

# "index": "data/index.json",
# "label": "data/label.json",
# "csv": "data/csv",
# "transform":"absolute", //"absolute" or "signed"
# "retain-weights":false,
# "threshold": "none"

indexFilename = config["index"]
labelFilename = config["label"]
CSVDirectory = config["csv"]

communiMethod = "louvain"
infomap_trials = 10
louvain_resolution = 1.0
louvain_quality_function = "modularity"
assymetricNegativeWeights = True

if("method" in config):
	communiMethod = config["method"].lower()

if("louvain-quality-function" in config and config["louvain-quality-function"]):
	louvain_quality_function = config["louvain-quality-function"].lower()

if("louvain-resolution" in config and isFloat(config["louvain-resolution"])):
	louvain_resolution = float(config["louvain-resolution"])

if("infomap-trials" in config and config["infomap-trials"]):
	infomap_trials = int(config["infomap-trials"])

if("assymetric-negative" in config):
	assymetricNegativeWeights = config["assymetric-negative"]

with open(indexFilename, "r") as fd:
	indexData = json.load(fd)

with open(labelFilename, "r") as fd:
	labelData = json.load(fd)


for entry in indexData:
	entryFilename = entry["filename"]

	alreadySigned = ("separated-sign" in entry) and entry["separated-sign"]

	#inputfile,outputfile,signedOrNot
	filenames = [entryFilename]
	baseName,extension = os.path.splitext(entryFilename)

	if(alreadySigned):
		filenames += [baseName+"_negative%s"%(extension)]

	if("null-models" in entry):
		nullCount = int(entry["null-models"])
		filenames += [baseName+"-null_%d%s"%(i,extension) for i in range(nullCount)]
		if(alreadySigned):
			filenames += [baseName+"_negative-null_%d%s"%(i,extension) for i in range(nullCount)]

	entry["community"] = True
	for filename in tqdm(filenames):
		adjacencyMatrix = loadCSVMatrix(os.path.join(CSVDirectory, filename))
		directionMode=ig.ADJ_DIRECTED
		weights = adjacencyMatrix
		if(check_symmetric(adjacencyMatrix)):
			directionMode=ig.ADJ_UPPER
			weights = weights[np.triu_indices(weights.shape[0], k = 0)]
		g = ig.Graph.Adjacency((adjacencyMatrix != 0).tolist(), directionMode)
		weighted = False
		if(not ((weights==0) | (weights==1)).all()):
			g.es['weight'] = weights[weights != 0]
			weighted = True

		weightsProperty = None
		signed = False;
		if(weighted):
			weightsProperty = "weight"
			if(np.any(np.array(g.es[weightsProperty])<0)):
				signed=True;
				g_pos = g.subgraph_edges(g.es.select(weight_gt = 0), delete_vertices=False)
				g_neg = g.subgraph_edges(g.es.select(weight_lt = 0), delete_vertices=False)
				g_neg.es['weight'] = [-w for w in g_neg.es['weight']]
				modularityWeights = [1,-1];
					
		if(communiMethod=="louvain"):
# 			optimiser = louvain.Optimiser()
# 				diff = optimiser.optimise_partition_multiplex(
# [part_pos, part_neg]
			hasResolution = False;
			partitionFunction = louvain.ModularityVertexPartition;
			if(louvain_quality_function=="modularity"):
				partitionFunction = louvain.ModularityVertexPartition;
				if(signed and assymetricNegativeWeights):
					modularityWeights = [1,-g_neg.ecount()/(g_pos.ecount()+g_neg.ecount())];
			elif(louvain_quality_function=="rbconfiguration"):
				partitionFunction = louvain.RBConfigurationVertexPartition;
				hasResolution = True;
				if(signed and assymetricNegativeWeights):
					modularityWeights = [1/g_pos.ecount(),-1.0/(g_pos.ecount()+g_neg.ecount())];
			elif(louvain_quality_function=="rber"):
				partitionFunction = louvain.RBERVertexPartition;
				hasResolution = True;
				if(signed and assymetricNegativeWeights):
					modularityWeights = [1/g_pos.ecount(),-1.0/(g_pos.ecount()+g_neg.ecount())];
			elif(louvain_quality_function=="cpm"):
				partitionFunction = louvain.CPMVertexPartition;
				hasResolution = True;
				if(signed and assymetricNegativeWeights):
					modularityWeights = [1/g_pos.ecount(),-1.0/(g_pos.ecount()+g_neg.ecount())];
			elif(louvain_quality_function=="significance"):
				partitionFunction = louvain.SignificanceVertexPartition;
				hasResolution = False;
				if(weighted):
					sys.exit("Significance quality does not work for weighted networks");
			elif(louvain_quality_function=="surprise"):
				partitionFunction = louvain.SurpriseVertexPartition;
				hasResolution = False;
				if(signed and assymetricNegativeWeights):
					modularityWeights = [1/g_pos.ecount(),-1.0/(g_pos.ecount()+g_neg.ecount())];
			else:
				sys.exit("Invalid louvain method.")
			
			if(signed):
				if(hasResolution):
					membership, improv = louvain_find_partition_multiplex([g_pos, g_neg],partitionFunction,
						layer_weights=modularityWeights,resolution_parameter=louvain_resolution,weights=weightsProperty)
				else:
					membership, improv = louvain_find_partition_multiplex([g_pos, g_neg],partitionFunction,
						layer_weights=modularityWeights,weights=weightsProperty)
			else:
				if(hasResolution):
					membership = louvain.find_partition(g,partitionFunction,
						weights=weightsProperty,resolution_parameter=louvain_resolution).membership
				else:
					membership = louvain.find_partition(g,partitionFunction,
						weights=weightsProperty).membership
		
		elif(communiMethod=="infomap"):
			if(signed):
				sys.exit("Infomap does not work for negative weights.")
			else:
				membership = g.community_infomap(edge_weights=weightsProperty,trials=infomap_trials).membership
		else:
			sys.exit("Invalid community detection method.")

		outputBaseName,outputExtension = os.path.splitext(filename)
		with open(os.path.join(csvOutputDirectory,"%s_community.txt"%os.path.basename(outputBaseName)), "w") as fd:
			for item in membership:
				fd.write("%d\n"%item)

		with open(os.path.join(csvOutputDirectory,os.path.basename(filename)), "w") as fd:
			if(weighted):
				outputData = g.get_adjacency(attribute='weight').data
			else:
				outputData = g.get_adjacency().data
			np.savetxt(fd,outputData,delimiter=",")

with open(os.path.join(outputDirectory,"index.json"), "w") as fd:
	json.dump(indexData,fd)

with open(os.path.join(outputDirectory,"label.json"), "w") as fd:
	json.dump(labelData,fd)

