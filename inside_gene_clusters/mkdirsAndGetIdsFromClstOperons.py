#!/usr/bin/python
import sys, fileinput
import os
import re


CREATED_DIRS = set()
AT_LEAST_ONE_DIR_CREATED = False


def initialyze(argv):
	global AT_LEAST_ONE_DIR_CREATED
	if str(argv[1]) == "help" or str(argv[1]) == "h":
		print USAGE
	for record in fileinput.input(argv[1]):
		recordList = record.split("\t")
		clst = recordList[0]
		protein = re.sub("^\d+_", "", recordList[1]).split("_")
		if (protein[0] != "XP" and protein[0] != "WP" and protein[0] != "NP" and protein[0] != "YP"):
			protein = protein[0]
		else:
			protein = "_".join(protein[0:2])
		dirName = "geneContext"+str(clst)
		if dirName not in CREATED_DIRS:
			if AT_LEAST_ONE_DIR_CREATED:
				os.chdir("..")
			else:
				AT_LEAST_ONE_DIR_CREATED = True
			os.mkdir(dirName)
			os.chdir(dirName)
			CREATED_DIRS.add(dirName)
		with open("geneContext.ids", "a+") as outFile:
			outFile.write(protein + "\n")
		

								
def main(argv):
	initialyze(argv)

				
			
if __name__ == "__main__":
	main(sys.argv)

