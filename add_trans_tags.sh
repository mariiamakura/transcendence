#!/bin/bash

# Function to process a single file
process_file() {
    local file="$1"

    # Check if the file exists and is a regular file
    if [ -f "$file" ]; then
        # Add {% trans %} tags to suitable text strings in the file
        sed -i -E 's/>([^<]+)</>{% trans '\''\1'\''  %}</g' "$file"
    fi
}

# Function to process all files in a directory recursively
process_directory() {
    local directory="$1"

    # Check if the directory exists
    if [ -d "$directory" ]; then
        # Process each file in the directory
        for file in "$directory"/*; do
            if [ -d "$file" ]; then
                # If it's a directory, recursively process it
                process_directory "$file"
            else
                # If it's a file, process it
                process_file "$file"
            fi
        done
    fi
}

# Function to remove content between trans and endtrans tags after adding trans-tags
#post_process() {
 #   local directory="$1"

    # Check if the directory exists
  #  if [ -d "$directory" ]; then
        # Process each file in the directory
   #     for file in "$directory"/*; do
    #        if [ -f "$file" ]; then
                # If it's a file, remove content between trans and endtrans tags
     #           remove_content "$file"
      #      fi
       # done
 #   fi
#}

# Main function to start processing
main() {
    local folder="$1"

    # Check if the folder path is provided
    if [ -z "$folder" ]; then
        echo "Usage: $0 <folder>"
        exit 1
    fi

    # Process the specified folder recursively
    process_directory "$folder"

    # Post-process to remove content between trans and endtrans tags
   # post_process "$folder"
}

# Call the main function with the provided folder path
chmod 777 app/frontend/templates/*
main "$1"
chmod 644 app/frontend/templates/*

