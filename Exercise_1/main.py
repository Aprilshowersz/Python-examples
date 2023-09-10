import os

# Paths for input and output files
input_file_path = "Exercise_1/file_to_read.txt"
output_file_path = "Exercise_1/result.txt"

# Open the input file for reading
with open(input_file_path, "r") as input_file:
    # Read the content of the file
    content = input_file.read()
    
    # Count the occurrences of "terrible"
    terrible_count = content.lower().count("terrible")
    
    # Initialize an empty list to store modified words
    modified_words = []
    
    # Iterate through words
    replace_flag = False
    for word in content.split():
        # Check if the word is "terrible"
        if word.lower() == "terrible":
            replace_flag = not replace_flag  # Toggle the replacement state
            if replace_flag:
                # Replace with "pathetic" on even occurrences
                modified_word = "pathetic"
            else:
                # Replace with "marvellous" on odd occurrences
                modified_word = "marvellous"
        else:
            modified_word = word
        
        # Add the modified word to the list
        modified_words.append(modified_word)
    
    # Join the modified words back into a string
    modified_content = " ".join(modified_words)

# Get the folder path of the output file
output_folder = os.path.dirname(output_file_path)

# If the output folder doesn't exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open the output file for writing
with open(output_file_path, "w") as output_file:
    # Write the modified content to the result file
    output_file.write(modified_content)

# Display the total count of "terrible"
print("Total count of 'terrible':", terrible_count)
