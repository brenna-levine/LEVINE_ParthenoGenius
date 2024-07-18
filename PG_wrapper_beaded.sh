#! /bin/bash

### The following wrapper script will run ParthenoGenius on all files contained 
### within a directory. This is useful if you have many offspring that you would like
### to evaluate for parthenogenesis.

#directory containing infiles for ParthenoGenius
# The below example is the directory containing all of the test files.
in_dir=ERROR-RATE-TESTS/CROC-PARTH-TESTS/INFILES/thin_50K


#Run ParthenoGenius on all input files in the directory
# For each file in the directory, run ParthenoGenius on the file, name the output file based on the name of the input 
#file, and use an error rate of 0.01
for file in $in_dir/*           
do			
	./ParthenoGenius.py $file $file'_0.100' --error 0.1 --P2_user_defined_error 0.1

done


