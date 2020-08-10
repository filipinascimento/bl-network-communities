#!/usr/bin/env python

import sys
import os.path
from os.path import join as PJ
import re
import json
import numpy as np
from tqdm import tqdm
import igraph as ig
import louvain
import math
import jgf
# import infomap


def isFloat(value):
	if(value is None):
		return False
	try:
		numericValue = float(value)
		return np.isfinite(numericValue)
	except ValueError:
		return False


class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
			np.int16, np.int32, np.int64, np.uint8,
			np.uint16, np.uint32, np.uint64)):
			ret = int(obj)
		elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
			ret = float(obj)
		elif isinstance(obj, (np.ndarray,)): 
			ret = obj.tolist()
		else:
			ret = json.JSONEncoder.default(self, obj)

		if isinstance(ret, (float)):
			if math.isnan(ret):
				ret = None

		if isinstance(ret, (bytes, bytearray)):
			ret = ret.decode("utf-8")

		return ret
results = {"errors": [], "warnings": [], "brainlife": [], "datatype_tags": [], "tags": []}

def warning(msg):
	global results
	results['warnings'].append(msg) 
	#results['brainlife'].append({"type": "warning", "msg": msg}) 
	print(msg)

def error(msg):
	global results
	results['errors'].append(msg) 
	#results['brainlife'].append({"type": "error", "msg": msg}) 
	print(msg)

def exitApp():
	global results
	with open("product.json", "w") as fp:
		json.dump(results, fp, cls=NumpyEncoder)
	if len(results["errors"]) > 0:
		sys.exit(1)
	else:
		sys.exit()

def exitAppWithError(msg):
	global results
	results['errors'].append(msg) 
	#results['brainlife'].append({"type": "error", "msg": msg}) 
	print(msg)
	exitApp()





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
outputFile = PJ(outputDirectory,"network.json.gz")

if(not os.path.exists(outputDirectory)):
		os.makedirs(outputDirectory)

with open(configFilename, "r") as fd:
		config = json.load(fd)


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

networks = jgf.igraph.load(config["network"], compressed=True)

outputNetworks = []

for network in tqdm(networks):
	weighted = "weight" in network.edge_attributes()
	layered = False
	if(weighted):
		signed = np.any(np.array(network.es["weight"])<0)
		if(signed):
			network_pos = network.subgraph_edges(network.es.select(weight_gt = 0), delete_vertices=False)
			network_neg = network.subgraph_edges(network.es.select(weight_lt = 0), delete_vertices=False)
			network_neg.es['weight'] = [-w for w in network_neg.es['weight']]
			layerNetworks = [network_pos,network_neg]
			layerWeights = [1,-1]
			layerNames = ["positive","negative"]
			layered=True
	if("layer" in network.edge_attributes()):
		if("edge-layer-weights" in network.attributes()):
			layerNames = list(network["edge-layer-weights"].keys())
			layerWeights = list(network["edge-layer-weights"].values())
		else:
			layerNames = list(set(network.es["layer"]))
			layerWeights = [1]*len(layerNames)
		layerNetworks = []
		for layerIndex,layerName in enumerate(layerNames):
			layerNetwork = network.subgraph_edges(network.es.select(layer_eq = layerName), delete_vertices=False)
			layerNetworks.append(layerNetwork)
		layered = True
	
	if(communiMethod=="louvain"):
# 			optimiser = louvain.Optimiser()
# 				diff = optimiser.optimise_partition_multiplex(
# [part_pos, part_neg]
		hasResolution = False
		if(layered):
			modularityWeights = layerWeights
		partitionFunction = louvain.ModularityVertexPartition
		if(louvain_quality_function=="modularity"):
			partitionFunction = louvain.ModularityVertexPartition
			if(layered and assymetricNegativeWeights):
				layerSizes = [g.ecount() for g in layerNetworks]
				allCount = np.sum(layerSizes)
				modularityWeights = [layerWeights[layerIndex]*layerSizes[layerIndex]/allCount for layerIndex in range(len(layerWeights))]
				modularityWeights[0] = 1.0
		elif(louvain_quality_function=="rbconfiguration"):
			partitionFunction = louvain.RBConfigurationVertexPartition
			hasResolution = True
			if(layered and assymetricNegativeWeights):
				layerSizes = [g.ecount() for g in layerNetworks]
				allCount = np.sum(layerSizes)
				modularityWeights = [layerWeights[layerIndex]/allCount for layerIndex in range(len(layerWeights))]
				modularityWeights[0] = 1.0/layerWeights[0]
		elif(louvain_quality_function=="rber"):
			partitionFunction = louvain.RBERVertexPartition
			hasResolution = True
			if(layered and assymetricNegativeWeights):
				layerSizes = [g.ecount() for g in layerNetworks]
				allCount = np.sum(layerSizes)
				modularityWeights = [layerWeights[layerIndex]/allCount for layerIndex in range(len(layerWeights))]
				modularityWeights[0] = 1.0/layerWeights[0]
		elif(louvain_quality_function=="cpm"):
			partitionFunction = louvain.CPMVertexPartition
			hasResolution = True
			if(layered and assymetricNegativeWeights):
				layerSizes = [g.ecount() for g in layerNetworks]
				allCount = np.sum(layerSizes)
				modularityWeights = [layerWeights[layerIndex]/allCount for layerIndex in range(len(layerWeights))]
				modularityWeights[0] = 1.0/layerWeights[0]
		elif(louvain_quality_function=="significance"):
			partitionFunction = louvain.SignificanceVertexPartition
			hasResolution = False
			if(weighted):
				sys.exit("Significance quality does not work for weighted networks")
		elif(louvain_quality_function=="surprise"):
			partitionFunction = louvain.SurpriseVertexPartition
			hasResolution = False
			if(layered and assymetricNegativeWeights):
				layerSizes = [g.ecount() for g in layerNetworks]
				allCount = np.sum(layerSizes)
				modularityWeights = [layerWeights[layerIndex]/allCount for layerIndex in range(len(layerWeights))]
				modularityWeights[0] = 1.0/layerWeights[0]
		else:
			sys.exit("Invalid louvain method.")
		
		if(layered):
			if(hasResolution):
				membership, improv = louvain_find_partition_multiplex(layerNetworks,partitionFunction,
					layer_weights=modularityWeights,resolution_parameter=louvain_resolution,weights="weight")
			else:
				membership, improv = louvain_find_partition_multiplex(layerNetworks,partitionFunction,
					layer_weights=modularityWeights,weights="weight")
		else:
			if(hasResolution):
				membership = louvain.find_partition(network,partitionFunction,
					weights="weight",resolution_parameter=louvain_resolution).membership
			else:
				membership = louvain.find_partition(network,partitionFunction,
					weights="weight").membership
	
	elif(communiMethod=="infomap"):
		if(signed):
			sys.exit("Infomap does not work for negative weights.")
		else:
			membership = network.community_infomap(edge_weights="weight",trials=infomap_trials).membership
	else:
		sys.exit("Invalid community detection method.")

	network.vs["Community"] = membership
	
	outputNetworks.append(network)

jgf.igraph.save(outputNetworks, outputFile, compressed=True)

