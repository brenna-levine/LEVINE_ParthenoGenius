#! /bin/bash

### The following wrapper script will run ParthenoGenius on all files contained 
### within a directory. This is useful if you have many offspring that you would like
### to evaluate for parthenogenesis.

#directory containing infiles for ParthenoGenius
# The below example is the directory containing all of the test files. To iterate through files in your own directory, change this path to the path to your directory.
in_dir=TUTORIAL/INFILES/


#Run ParthenoGenius on all input files in the directory
# For each file in the directory, run ParthenoGenius on the file, name the output file based on the name of the input 
#file, and use an error rate of 0.01 for Part 1 and an error rate of 0.01 for Part 2.

for file in $in_dir/*           
do			
	./ParthenoGenius.py $file $file --error 0.01 --P2_user_defined_error 0.01
done


