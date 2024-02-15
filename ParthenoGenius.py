#!/usr/bin/env python
# coding: utf-8

############## create argument parser #################
#import argparse library
import argparse

#create an argument parser object
parser=argparse.ArgumentParser(description='ParthenoGenius')

#add positional arguments to argument parser (i.e., the required information)
parser.add_argument('infile', help="csv file with maternal and offspring alleles - See README for format")
parser.add_argument('outfile', help="prefix for naming output files")
parser.add_argument('--error', help="per base error rate; default = 0.001; see README for explanation", nargs="?", const=1, default=0.001)

#parse arguments
args=parser.parse_args()

###################### read data and define parameters #########################

#import pandas
import pandas

#read in command line argument of infile and assign contents to a variable
with open(args.infile) as data_file:
    structure_alleles = pandas.read_csv(data_file, index_col=0)

#name output files
outfile_homozyg_part1 = "%s.part1.homozygosity_scan_raw.txt" % args.outfile
outfile_locus_scan = "%s.part1.homozygosity_scan_summary.txt" % args.outfile
outfile_heterozyg_part2 = "%s.part2.heterozygosity_scan_raw.txt" % args.outfile
outfile_heterozyg_sum_part2 = "%s.part2.heterozygosity_scan_summary.txt" % args.outfile

#get date and time of run
from datetime import datetime
now = datetime.now()
now_str = now.strftime("%d/%m/%Y %H:%M:%S")

#count number of rows in dataframe
row_total = structure_alleles.shape[0]
#print(row_total)

#count number of columns (loci)
column_total = structure_alleles.shape[1]
#print(column_total)

#########################################################################################
#########################################################################################
######################################### PART 1 ########################################
################################# scan for offspring alleles differing from maternal homozygous genotypes ###############################

#declare empty list to hold names of loci for which mom is homozygous
mom_homozyg = [] 

#declare empty list to hold male alleles 
males_homo = []

#declare value for missing data
missing_data = -9 ###### ADDITION 27 NOV 23 - coding in missing data as "-9" ##################


with open(outfile_homozyg_part1, 'w') as fileobject: #with homozygous loci file open for writing

    #write statements to outfile to appear before loci are returned 
    fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: PART 1 MATERNAL HOMOZYGOUS LOCI SCAN ########\n")
    fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
    fileobject.write(f"######## Data generated: (D/M/Y) {now_str} #########\n\n\n")
    fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tError = {args.error}\n\n\n")
    fileobject.write(f"The following are the IDs for the loci at which the mom is homozygous. Loci at which the mom or offspring have missing data are not included.\n")
    fileobject.write(f"If an offspring allele differs from the maternal homozygous genotype, the incongruous maternal allele and offspring allele are printed below the locus.\n\n")
    fileobject.write(f"Please refer to the maternal homozygous loci scan summary output file for summary statistics.\n\n\n")
    
    for (columnName, columnData) in structure_alleles.iteritems():  #for column/value pair
   
        mom1 = columnData.values[0] #mom1 = mom allele 1
        mom2 = columnData.values[1] #mom2 = mom allele 2
    
        #NEW ADDITION - 27 NOV 23 - added ability to deal with missing data (-9)
        if mom1 == mom2 and mom1 != missing_data and columnData.values[2] != missing_data and columnData.values[3] != missing_data: #if mom is homozygous and if she's not missing data and the offspring isn't missing data at the homozygous locus - i.e., if the mom's two alleles at the locus are identical, the identical data aren't missing data, and the offspring isn't missing data here either
        
            fileobject.write(f"Locus: {columnName}\n\n") #write the locus name to the outfile
            mom_homozyg.append(columnName) #append the name of the locus to the mom_homozyg list
        
            if mom1 != columnData.values[2] or mom1 != columnData.values[3]: #if mom homozygous allele does not equal one or or both offspring alleles  
               
                #write statements about maternal and offspring alleles to outfile
                fileobject.write(f"\tMom homozygous allele: {mom1}")
                fileobject.write(f"\n\tOffspring allele 1: {columnData.values[2]}")
                fileobject.write(f"\n\tOffspring allele 2: {columnData.values[3]}\n\n")
                
                males_homo.append(columnData.values[2]) #append one of the male alleles to males list - doesn't matter which one because it is just for counting


#close fileobject
fileobject.close()


############ BEGIN NEW ADDITIONS - 2 NOVEMBER 2022 ######################
### the following allows for the calculation of Blouin's Mxy (Genotype Sharing Index)
### Per Blouin et al. 1996, values can range from 0 to 2 (i.e., no identical alleles to completely identical genotypes at all loci)

#declare list to hold all alleles shared by mom and offspring
shared_alleles = []

for (columnName, columnData) in structure_alleles.iteritems():  #for column/value pair
   
    mom1 = columnData.values[0] #mom1 = mom allele 1
    mom2 = columnData.values[1] #mom2 = mom allele 2
    
    if mom1 != mom2 and mom1 != missing_data and mom2 != missing_data and columnData.values[2] != missing_data and columnData.values[3] != missing_data: #if mom is heterozygous and doesn't have missing data and the offspring isn't missing data at these loci as well - i.e., if the mom's two alleles at the locus are not identical
        
        if mom1 == columnData.values[2] and mom2 == columnData.values[3]: #if mom allele 1 = offspring allele 1 and mom allele 2 = offspring allele 2  

            shared_alleles.append(columnData.values[2]) #append shared offspring allele to shared list
            shared_alleles.append(columnData.values[3]) #append shared offspring allele to shared list

        elif mom1 == columnData.values[3] and mom2 == columnData.values[2]: #if mom allele 1 = offspring allele 2 and mom allele 2 = offspring allele 1 

            shared_alleles.append(columnData.values[2]) #append shared offspring allele to shared list
            shared_alleles.append(columnData.values[3]) #append shared offspring allele to shared list

        elif mom1 == columnData.values[2] and mom2 != columnData.values[3]: #if mom allele 1 = offspring allele 1, but mom allele 2 != offspring allele 2

            shared_alleles.append(columnData.values[2]) #append shared offspring allele to shared list

        elif mom1 != columnData.values[2] and mom2 == columnData.values[3]: #if mom allele 1 != offspring allele 1, but mom allele 2 = offspring allele 2

            shared_alleles.append(columnData.values[3]) #append shared offspring allele to shared list 

        elif mom1 == columnData.values[3] and mom2 != columnData.values[2]: #if mom allele 1 = offspring allele 2, but mom allele 2 != offspring allele 1

            shared_alleles.append(columnData.values[3]) #append shared offspring allele to shared list  

        elif mom1 != columnData.values[3] and mom2 == columnData.values[2]: #if mom allele 1 != offspring allele 2, but mom allele 2 = offspring allele 1

            shared_alleles.append(columnData.values[2]) #append shared offspring allele to shared list         

    elif mom1 == mom2 and mom1 != missing_data and columnData.values[2] != missing_data and columnData.values[3] != missing_data: #if mom is homozygous and isn't missing data and the offspring isn't missing data at these loci either - i.e., if the mom's two alleles at the locus are identical

        if mom1 == columnData.values[2] and mom1 == columnData.values[3]: #if the mom allele matches both alleles of the offspring at the locus

            shared_alleles.append(columnData[2]) #append the shared offspring allele to the shared list
            shared_alleles.append(columnData[3]) #append the shared offspring allele to the shared list

        elif mom1 == columnData.values[2] and mom1 != columnData.values[3]: #if mom allele matches only the first allele of the offspring

            shared_alleles.append(columnData[2]) #append the shared offspring allele to the shared list

        elif mom1 != columnData.values[2] and mom1 == columnData.values[3]: #if mom allele matches only the second offspring structure_alleles

            shared_alleles.append(columnData[2]) #append the shared offspring allele to the shared list

#calculate number of alleles shared between mom and offspring
num_shared = len(shared_alleles)

########## END NEW ADDITIONS - 2 NOV 2022 ###############

 
with open(outfile_locus_scan, 'w') as fileobject: #with homozygosity summary outfile open for writing
    #write summary statistics about the data to the outfile
    fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: SUMMARY OF HOMOZYGOUS LOCUS SCAN ########\n")
    fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
    fileobject.write(f"######## Data generated: (D/M/Y) {now_str} #########\n\n\n") #write the date and time to the outfile
    fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tError = {args.error}\n\n\n")
        
    fileobject.write(f"Total number of loci in input file scanned (may include loci with missing data): {column_total}\n\n\n") 

    fileobject.write(f"THE FOLLOWING STATS REFERS ONLY TO LOCI AT WHICH NEITHER THE MOTHER NOR OFFSPRING HAVE MISSING DATA:\n\n")
    fileobject.write(f"\tNumber of loci for which mom is homozygous and offspring are not missing data: {len(mom_homozyg)}\n")
    fileobject.write(f"\tNumber of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles: {len(males_homo)}\n")
    fileobject.write(f"\tMaximum number of homozygous loci expected to differ between mom and offspring based on error rate: {round((len(mom_homozyg))*float(args.error), 5)}\n")
    fileobject.write(f"\tProportion of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles: {round(len(males_homo)/len(mom_homozyg), 5)}\n")
    fileobject.write(f"\tProportion of mom's homozygous loci for which offspring has identical homozygous genotypes to maternal homozygous genotypes: {round(1 - (len(males_homo)/len(mom_homozyg)), 5)}\n\n\n")

    
    #### END NEW ADDITION 2 NOV 2022 #########    

    #Test for significance - if proportion on mom's homozygous loci for which at least one of male's alleles differ from maternal alleles is less
    #than or equal to default or user-defined sequencing error rate, call a likely parthenogen
    if ((len(males_homo)) <= (float(args.error)*len(mom_homozyg))):
        fileobject.write(f"THE OFFSPRING IS LIKELY A PARTHENOGEN.\n")
        fileobject.write(f"\n\tThe number of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles is less than expected from the genotyping error rate alone.\n")
        fileobject.write(f"\tIncongruence between maternal genotypes and offspring genotypes is likely due to genotyping error rather than the presence of paternal alleles.")
    else:
        fileobject.write(f"THE OFFSPRING IS UNLIKELY TO BE A PARTHENOGEN.\n")
        fileobject.write(f"\n\tThe number of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles is greater than the number expected from the genotyping error rate alone.\n")
        fileobject.write(f"\tIncongruence between maternal genotypes and offspring genotypes may be due to presence of paternal alleles.\n\n\n")
        fileobject.write(f"Note: Part 2 maternal heterozygosity analysis will not be conducted to test for mode of parthenogenesis.\n")
        fileobject.write(f"Note: Part 2 heterozygosity outfiles will not be created.")

#close fileobject
fileobject.close()

#calculate estimated genotyping error rate by dividing number of male loci that differ from mom homozygous genotype
estim_error = len(males_homo)/len(mom_homozyg)

#######################################################################################################
#######################################################################################################
##################################### PART 2 - scan for maternal heterozygosity if evidence of parthenogenesis ##################################
########################################################################################################

    
if ((len(males_homo)) <= (float(args.error)*len(mom_homozyg))): #if evidence of parthenogenesis

    #declare empty list to hold loci names for which mom is heterozygous
    mom_het = [] 

    #reset males list to empty; this list will be populated by one male allele for each locus at which a male is homozygous for a maternal allele at a maternal heterozygous locus
    males = []

    with open(outfile_heterozyg_part2, 'w') as fileobject: #with heterozygous loci outfile open for writing

        #write statements to outfile to appear before loci are returned 
        fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: HETEROZYGOUS LOCI #########\n")
        fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
        fileobject.write(f"######## Data generated: (D/M/Y) {now_str} #########\n\n\n") #write date and time to outfile
        fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tEstimated Error Rate from Part 1 Maternal Locus Scan = {round(estim_error, 5)}\n\n\n")
        fileobject.write(f"The following are the IDs for the loci at which the mom is heterozygous. Loci at which the mother or offspring have missing data are not included.\n") 
        fileobject.write(f"If the offspring is heterozygous for the mom's alleles, the mom's and offspring's alleles are printed below.\n\n")
        fileobject.write(f"Please refer to the maternal heterozygous loci summary output file for summary statistics.\n\n")
            
        for (columnName, columnData) in structure_alleles.iteritems():  #for column/value pair
       
            mom1 = columnData.values[0] #mom1 = mom allele 1
            mom2 = columnData.values[1] #mom2 = mom allele 2
        
            if mom1 != mom2 and mom1 != missing_data and mom2 != missing_data and columnData.values[2] != missing_data and columnData.values[3] != missing_data: #if mom is heterozygous - i.e., if the mom's two alleles at the locus are not identical
            
                fileobject.write(f"Locus: {columnName}\n\n") #write the locus name to the outfile
                mom_het.append(columnName) #append the locus name to the mom_het list
            
                if mom1 == columnData.values[2] and mom2 == columnData.values[3]: #if mom allele 1 = offspring allele 1 and mom allele 2 = offspring allele 2  

                    #write data to the outfile
                    fileobject.write(f"\tMom allele 1: {mom1}") 
                    fileobject.write(f"\n\tMom allele 2: {mom2}") 
                    fileobject.write(f"\n\tOffspring allele 1: {columnData.values[2]}") 
                    fileobject.write(f"\n\tOffspring allele 2: {columnData.values[3]}\n\n")

                    males.append(columnData.values[3]) #append male allele to males list

                elif mom1 == columnData.values[3] and mom2 == columnData.values[2]: #if mom allele 1 = offspring allele 2 and mom allele 2 = offspring allele 1 

                    #write data to the outfile
                    fileobject.write(f"\tMom allele 1: {mom1}") 
                    fileobject.write(f"\n\tMom allele 2: {mom2}") 
                    fileobject.write(f"\n\tOffspring allele 1: {columnData.values[2]}") 
                    fileobject.write(f"\n\tOffspring allele 2: {columnData.values[3]}\n\n")

                    males.append(columnData.values[2]) #append male allele to males list


    #close the fileobject
    fileobject.close()

    with open(outfile_heterozyg_sum_part2, 'w') as fileobject: #with the heterozygosity summary outfile open for writing
        
        #write statements to outfile
        fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: HETEROZYGOUS LOCI SUMMARY #########\n")
        fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
        fileobject.write(f"######## Data generated: (D/M/Y) {now_str} #########\n\n\n")
        fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tEstimated Error Rate from Part 1 Maternal Locus Scan = {round(estim_error, 5)}\n\n\n")
        fileobject.write(f"SUMMARY: SCAN OF MATERNAL HETEROZYGOUS LOCI FOR OFFSPRING RETAINED HETEROZYGOSITY\n\n")
        fileobject.write(f"Total number of loci in input file scanned: {column_total}\n")
        fileobject.write(f"Number of loci in input file with missing data: {column_total-(len(mom_het)+len(mom_homozyg))}\n")
        fileobject.write(f"Total number of loci for which mom and offspring do not have missing data: {len(mom_het)+len(mom_homozyg)}\n")
        fileobject.write(f"Number of loci for which mom is heterozygous: {len(mom_het)}\n") #print total number of loci
        fileobject.write(f"Number of mom's heterozygous loci for which offspring has retained maternal heterozygosity: {len(males)}\n") #print number of loci for which all males have paternal alleles
        fileobject.write(f"Maximum number of mom's heterozygous loci expected to be heterozygous in offspring assuming null hypothesis of gametic duplication: {round((len(mom_het))*float(estim_error), 3)}\n")
        fileobject.write(f"Minimum number of mom's heterozygous loci expected to be heterozygous in offspring assuming alternative hypothesis of central fusion automixis (based on retained heterozyosity assumption of 66%): {round((len(mom_het))*float(0.66), 3)}\n")
        fileobject.write(f"Range of numbers of mom's heterozygous loci expected to be heterozygous in offspring assuming alternative hypothesis of terminal fusion automixis: > {round((len(mom_het))*float(estim_error), 3)} - < {round((len(mom_het))*float(0.66), 3)}\n")
        fileobject.write(f"Minimum number of mom's heterozygous loci expected to be heterozygous in offspring assuming alternative hypothesis of endoduplication: >= {round((len(mom_het))*(1-float(estim_error)), 3)}\n")
        fileobject.write(f"Proportion of mom's heterozygous loci for which offspring has retained heterozygosity: {round(len(males)/len(mom_het), 3)}\n\n")


        #### BEGIN NEW ADDITION 2 NOV 2022#######
        fileobject.write(f"Genotype Sharing Index (Mxy):\n")
        fileobject.write(f"\tPer Blouin et al. 1996, Mxy ranges from 0 - 2, as individuals can share up to 2 alleles per locus\n\n")
        fileobject.write(f"\t\tMxy: {round((num_shared/(len(mom_het)+len(mom_homozyg))), 5)}\n\n\n")

        #Test for significance - if proportion on mom's heterozygous loci for which male is heterozygous differ is less
        #than or equal to default or user-defined sequencing error rate, call a likely parthenogen
        if ((len(males)) > (float(estim_error)*len(mom_het))) and ((len(males)) < (float(0.67)*len(mom_het))): #######EDITED 27 NOV 23
            fileobject.write(f"This parthenogen was likely produced via:\tTERMINAL FUSION AUTOMIXIS\n\n")
            fileobject.write(f"\tThe number of mom's heterozygous loci for which offspring has retained heterozygosity is greater than the number expected based on estimated error rate alone assuming a null hypothesis of gametic duplication and less than the number expected given an alternative hypothesis of central fusion automixis (assuming at last 66% retained maternal heterozygosity).\n")
        elif ((len(males)) >= (float(0.67)*len(mom_het))) and ((len(males) < ((1-float(estim_error))*len(mom_het)))) : #######EDITED 7 FEB 23
            fileobject.write(f"This parthenogen was likely produced via:\tCENTRAL FUSION AUTOMIXIS\n\n")
            fileobject.write(f"\tThe number of mom's heterozygous loci for which offspring has retained heterozygosity is greater than the number expected given an alternative hypothesis of central fusion automixis (assuming at least 66% retained maternal heterozygosity).\n")
        elif ((len(males)) >= ((1-float(estim_error))*len(mom_het))): #######EDITED 7 FEB 24
            fileobject.write(f"This parthenogen was likely produced via:\tENDODUPLICATION\n\n")
            fileobject.write(f"\tThe number of mom's heterozygous loci for which offspring has retained heterozygosity is greater than the number expected considering genotyping error and an alternative hypothesis of endoduplication.\n\n")
            fileobject.write(f"***Note: 100% retention of maternal heterozygosity is also a potential outcome of central fusion automixis, but it is highly unlikely as it would require zero recombination.")
        else:
            fileobject.write(f"This parthenogen was likely produced via:\tGAMETIC DUPLICATION\n\n")
            fileobject.write(f"\tThe number of mom's heterozygous loci for which offspring has retained heterozygosity is less than the number expected based on estimated error rate alone assuming a null hypothesis of gametic duplication.\n")
            fileobject.write(f"\tTherefore, any apparent offspring heterozygosity at these loci is likely an artifact of error.")
           

    #close the fileobject
    fileobject.close()
