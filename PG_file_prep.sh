#! /bin/bash
############### This script generates a series of input files for ParthenoGenius
############### Two input files must be in your directory: genotypes.csv and ID_pairs.txt
############### See README for info about these files

#store input file names as variables
ID_pairs=ID_pairs.txt    #file containing the names of the mom/offspring pairs
genotypes=genotypes.csv  #file containing genotypes for the individuals in the pairs

#extract offspring IDs (no header/case insensitive) and write to a temporary file
cut -f 1 $ID_pairs | grep -v -i OFFSPRING_ID > offspring_list

###create offspring array
COUNTER=0 #set counter to 0
while read line #while reading lines in the offspring_list file
do 
	off_array[$COUNTER]=$line	#assign value of line to offspring array element
	COUNTER=$((COUNTER+1))	#increase counter by 1
done < offspring_list #feed the offspring_list to the while loop

#remove temporary file
#rm offspring_list

#print array to confirm you now have an array of offspring IDs
#echo ${off_array[*]}

#extract mom IDs (no header/case insensitive) and assign to a temporary file
cut -f 2 $ID_pairs | grep -v -i MOM_ID > mom_list

###create mom array
COUNTER=0 #reset counter to 0
while read line #while reading lines in the mom_list file
do 
	mom_array[$COUNTER]=$line	#assign value of line to mom array element
	COUNTER=$((COUNTER+1))	#increase counter by 1
done < mom_list #feed the mom_list to the while loop

#remove temporary file
rm mom_list

#print array to confirm you now have an array of mom IDs
#echo ${mom_array[*]}

#get number of elements in the offspring array
off_num=${#off_array[@]}

#print number of elements in offspring array to confirm
#echo $off_num

##create ParthenoGenius input files for each mother/offspring pair
COUNTER=0 #set counter to 0
while [ $COUNTER -lt $off_num ] #while value of the counter is less than number of elements in offspring array
do
	head -n1 $genotypes > ${off_array[$COUNTER]}_PG_input.csv #write header of genotypes file to new file for each mom/offspring pair
	grep "${mom_array[$COUNTER]}," $genotypes >> ${off_array[$COUNTER]}_PG_input.csv #write mom's genotypes to new file for each mom/offspring pair
	grep "${off_array[$COUNTER]}," $genotypes >> ${off_array[$COUNTER]}_PG_input.csv #write offspring's genotypes to new file for each mom/offspring pair
	#echo ${off_array[$COUNTER]}_PG_input.csv >> input_file_list.txt #write file name to a file for ParthenoGenius to iterate through
	COUNTER=$((COUNTER+1)) #increase counter by 1
done


