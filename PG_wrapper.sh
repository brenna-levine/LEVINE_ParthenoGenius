#! /bin/bash

in_dir=NEPALESE-VIPER-PARTH-TESTS/INFILES
out_dir=NEPALESE-VIPER-PARTH-TESTS/OUTFILES

#feed all ParthenoGenius input files to ParthenoGenius
for file in $in_dir/*
do
	python3 ParthenoGenius.py $file $file --error 0.01
done

# mkdir $out_dir/parths
# mkdir $out_dir/non_parths

# for file in $in_dir/*
# do
# 	if [[ "$file" == *"$part"* ]]; then
# 		mv $file $out_dir/
# 	#else 
# 		#mv $file.part* ../$out_dir/non_parths/
# 	fi
# done