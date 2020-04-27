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

if("method" in config):
	communiMethod = config["method"].lower()

if("louvain-quality-function" in config and config["louvain-quality-function"]):
	louvain_quality_function = config["louvain-quality-function"].lower()

if("louvain-resolution" in config and isFloat(config["louvain-resolution"])):
	louvain_resolution = float(config["louvain-resolution"])

if("infomap-trials" in config and config["infomap-trials"]):
	infomap_trials = int(config["infomap-trials"])

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
		if(weighted):
			weightsProperty = "weight"
		
		if(communiMethod=="louvain"):
			if(louvain_quality_function=="modularity"):
				membership = louvain.find_partition(g,louvain.ModularityVertexPartition, weights=weightsProperty).membership
			elif(louvain_quality_function=="rbconfiguration"):
				membership = louvain.find_partition(g,louvain.RBConfigurationVertexPartition,
					weights=weightsProperty, resolution_parameter=louvain_resolution).membership
			elif(louvain_quality_function=="rber"):
				membership = louvain.find_partition(g,louvain.RBConfigurationVertexPartition,
					weights=weightsProperty, resolution_parameter=louvain_resolution).membership
			elif(louvain_quality_function=="cpm"):
				membership = louvain.find_partition(g,louvain.CPMVertexPartition,
					weights=weightsProperty, resolution_parameter=louvain_resolution).membership
			elif(louvain_quality_function=="significance"):
				membership = louvain.find_partition(g,louvain.SignificanceVertexPartition).membership
			elif(louvain_quality_function=="surprise"):
				membership = louvain.find_partition(g,louvain.SurpriseVertexPartition,
					weights=weightsProperty).membership
			else:
				sys.exit("Invalid louvain method.")
		elif(communiMethod=="infomap"):
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

