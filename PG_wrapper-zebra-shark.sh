#! /bin/bash

### The following wrapper script will run ParthenoGenius on all files contained 
### within a directory. This is useful if you have many offspring that you would like
### to evaluate for parthenogenesis.

#directory containing infiles for ParthenoGenius
# The below example is the directory containing all of the test files.
in_dir=ZEBRA-SHARK-PARTH-TESTS/INFILES


#Run ParthenoGenius on all input files in the directory
# For each file in the directory, run ParthenoGenius on the file, name the output file based on the name of the input 
#file, and use an error rate of 0.01
for file in $in_dir/*           
do			
	python3 ParthenoGenius.py $file $file --error 0.01
done


