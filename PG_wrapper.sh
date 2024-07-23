#! /bin/bash

### The following wrapper script will run ParthenoGenius on all files contained 
### within a directory. This is useful if you have many offspring that you would like
### to evaluate for parthenogenesis.

#! /bin/bash

# Check if the required parameters (input directory, output directory, and part 1 error rate) are provided and if the optional part 2 error rate parameter is provided
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
    echo "Usage: $0 <input_directory> <output_directory> <Part_1_error_rate> [P2_user_defined_error]"
    echo "Required arguments: <input_directory> <output_directory> <Part_1_error_rate>"
    echo "Visit https://github.com/brenna-levine/LEVINE_ParthenoGenius for help."
    exit 1
fi

# Create temporary variable containing infiles directory for ParthenoGenius
in_dir=$1

# Create temporary variable containing outfiles directory for ParthenoGenius
out_dir=$2

# Create temporary variable containing error rate
error_rate=$3

# If there is an optional P2_user_defined_error parameter, assign it to a temporary variable
if [ -n "$4" ]; then
    P2_user_defined_error=$4
fi

# Create an output directory for the outfiles if it doesn't exist
mkdir -p $out_dir

# Run ParthenoGenius on all input files in the directory
for file in $in_dir/*  #for all files in the input directory         
do
    outfile="${out_dir}/$(basename "$file")"
    if ./ParthenoGenius.py "$file" "$outfile" --error "$error_rate" --P2 "$P2_user_defined_error"; then
        echo "Processed $file successfully with ParthenoGenius."
    else
        echo "Failed to process $file with ParthenoGenius." >&2
    fi
done


