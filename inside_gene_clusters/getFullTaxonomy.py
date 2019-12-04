#!/usr/bin/python
import sys, fileinput
import collections
from ete2 import NCBITaxa
import os
import re
ncbi = NCBITaxa()

USAGE = sys.argv[0] + "input-file with organism names" + "taxonomy source: NCBI or GDTB" +  ">" +  "output-file" 
# Currently: NCBI or GTDB
TAXONOMY_SOURCE = "NCBI"
ORGANISM_NAME_TO_AMMOUNT = collections.defaultdict(int)
ORGANISM_NAME_TO_ORIGINAL_NAME = {}
ORGANISM_NAMES_LIST = []
GTDB_TAXONOMY_FILE = "/".join(os.path.realpath(__file__).split("/")[:-1]) + "/ar122_bac120_metadata_r89_taxonomy.tsv"

# Update taxonomy database if needed
# ncbi.update_taxonomy_database()

def initialyze(argv):
	if str(argv[1]) == "help" or str(argv[1]) == "h":
		print USAGE
		exit()
	global TAXONOMY_SOURCE
	TAXONOMY_SOURCE = argv[2]
	for name in fileinput.input(argv[1]):
		if len(name.strip()):
			organismName = " ".join(name.strip().split("_"))
		if TAXONOMY_SOURCE == "NCBI":
			ORGANISM_NAMES_LIST.append(organismName)
		elif TAXONOMY_SOURCE == "GTDB":
			orgName = " ".join(organismName.split("_"))
			ORGANISM_NAME_TO_AMMOUNT[organismName.lower()] += 1
			ORGANISM_NAME_TO_ORIGINAL_NAME[organismName.lower()] = organismName
		

def getNcbiTaxonomy():	
	nameToTaxIdList = ncbi.get_name_translator(ORGANISM_NAMES_LIST)
	for name, taxIds in nameToTaxIdList.items():
		for eachId in taxIds:
			lineage = ncbi.get_lineage(str(eachId))
			names = ncbi.get_taxid_translator(lineage)
			print ("\t".join([names[taxid] for taxid in lineage]))


def getGTDBTaxonomy():
	with open(GTDB_TAXONOMY_FILE, "r") as gtdbTaxonomyFile:
		for line in gtdbTaxonomyFile:
			line = line.split("\t")
			ncbiTaxonomy = line[1].split(";")
			gtdbTaxonomy = line[2].split(";")
			ncbiNameLower = ncbiTaxonomy[-1].strip().lower()
			gtdbNameLower = gtdbTaxonomy[-1].strip().lower()
			ncbiNameLower = re.sub("^.__", "", ncbiNameLower)
			gtdbNameLower = re.sub("^.__", "", gtdbNameLower)
			if ncbiNameLower in ORGANISM_NAME_TO_AMMOUNT:
				printGDTBTaxonomy(ncbiNameLower, gtdbTaxonomy)
			elif gtdbNameLower in ORGANISM_NAME_TO_AMMOUNT:
				printGDTBTaxonomy(gtdbNameLower, gtdbTaxonomy)
		# print organisms for which retrieving of taxonomy was not successfull
		for organism in ORGANISM_NAME_TO_AMMOUNT:
			print ORGANISM_NAME_TO_ORIGINAL_NAME[organism] + " ======================= Taxonomy Not Found"


def printGDTBTaxonomy(name, gtdbTaxonomy):
	for organismCount in xrange(ORGANISM_NAME_TO_AMMOUNT[name]):
		print ("\t".join(gtdbTaxonomy))	
	# delet the organism from the dictionary, indicating
	# that the taxonomy was retrieved successfully
	del ORGANISM_NAME_TO_AMMOUNT[name]
		
						
def main(argv):
	initialyze(argv)
	if TAXONOMY_SOURCE == "NCBI":
		getNcbiTaxonomy()
	elif TAXONOMY_SOURCE == "GTDB":
		getGTDBTaxonomy()
				
			
if __name__ == "__main__":
	main(sys.argv)
