#!/usr/bin/python
# drugability tool


# Version 1.0beta
# David YunTe Lin (dlin@nygenome.org)
# New York Genome Center


import sys
import os
#import panda



def print_pipeline_message(message):
    print '\n======================================================================================================='
    print message
    print '=========================================================================================================\n'

print_pipeline_message("This tool will search the database for potential drugs. Please have your project file ready")

wgs_list = []
cnv_list = []
drug_list = []
cancer_list= []

parent = "/data/analysis/CLIA/"
path_to_drug = "/nethome/dlin/cancer_alliance/Drug_Targets_Kaz_2016-02-03.txt"
path_to_cancer = "/nethome/dlin/cancer_gene_census.genes.txt"
path_to_project = os.getcwd()

with open(path_to_drug, 'r') as drug:
	for item in drug.readlines():
		item = item.strip()
		item = item.split()
		drug_list.append(item)
drug.close()

with open(path_to_cancer, 'r') as cancer:
	for gene in cancer.readlines():
		gene = gene.strip()
		gene = gene.split()
		cancer_list.append(','.join(gene))
cancer.close()

#sys.exit(0)

os.chdir(path_to_project)

print "You are working at: %s" % os.getcwd()

if len(sys.argv) == 1:
	print "I need a list of Projects,", "you can also give filename as a command line argument"
	file_list = raw_input("Enter Filename: ")
else:
	file_list = sys.argv[1]

#sys.exit(0)

file_count = 0
with open(file_list, 'r') as wanted:
	for sample in wanted.readlines():
		if not sample.startswith("#"):
			sample = sample.strip()
			sample = sample.split()
			path1 = parent + sample[0] + "/" + sample[1] + "/" + "analysis/"
			path2 = parent + sample[0] + "/" + sample[1] + "/" + "summary/"
			for file in os.listdir(path1):
				if file.endswith("W.union.v5B.annotated.txt") or file.endswith("E.union.v5B.annotated.txt") or file.endswith("D.union.v5B.annotated.txt"):
					data = path1+file
					wgs_list.append(data)
					var_filter = []
					to_open = path1+"%s_druggable.txt"%file
					print "Processing", to_open
					file_count += 1
					out_file1 = open(to_open, 'w')
					#print out_file1
					with open(data, 'r') as file_to_parse1:
						cancer_gene = []
						head1 = file_to_parse1.readline()
						print>>out_file1, (head1.strip() + "\t" + "cancer_census" + "\t" + "drug").strip()
						cancer_gene.append(head1)
						for var in file_to_parse1.readlines():
							var = var.strip()
							var = var.split()
							var_filter.append(var)
					file_to_parse1.close()
					for var in var_filter:
						if var[6] in cancer_list:
							new_line = '\t'.join(var) + "\t" + "Yes"
							cancer_gene.append(new_line)
						else:
							new_line = '\t'.join(var) + "\t" + "No"
							cancer_gene.append(new_line)
						# for item in drug_list:
							# if var[6] == item[0]: 
								# print>>out_file1, '\t'.join(var) + "\t" + item[2]
								# drugable.append('\t'.join(var) + "\t" + item[2])
					for item in cancer_gene:
						item = item.strip()
						item = item.split()
						for drug in drug_list:
							if item[6] == drug[0]:
								print>>out_file1, '\t'.join(item) + "\t" + drug[2]
					out_file1.close()
			for file in os.listdir(path2):
				if file.endswith("W.cnv.genes.log2") or file.endswith("E.cnv.genes.log2"):
					data = path2+file
					cnv_list.append(data)
					cnv_filter = []
					to_open = path2+"%s_drugable.txt"%file
					print "Processing",to_open
					file_count += 1
					out_file2 = open(to_open, 'w')
					#print out_file2
					with open(data, 'r') as file_to_parse2:
						head2 = "GeneID" + "\t" + "log2" + "\t" + "chr:position" + "\t" + "scale" + "\t" + "score" +"\t" +"drugs"
						print>>out_file2, head2.strip()
						for cnv in file_to_parse2.readlines():
							cnv = cnv.strip()
							cnv = cnv.split()
							cnv_filter.append(cnv)
					file_to_parse2.close()
					for cnv in cnv_filter:
						for item in drug_list:
							if cnv[0] == item[0]:
								print>>out_file2, '\t'.join(cnv) + "\t" + item[2]
					out_file2.close()



print
print file_count, "files processed at", parent
