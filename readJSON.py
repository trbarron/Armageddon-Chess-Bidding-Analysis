# Path to your large JSON file
file_path = 'lichess_db_standard_rated_2014-09.json'

# Open the file
with open(file_path, 'r') as file:
    # Initialize a counter for the number of lines read
    line_count = 0

    # Read the file line by line
    for line in file:
        # Print the current line
        print(line)  # 'end' argument is used to avoid adding extra newline characters

        # Increment the line counter
        line_count += 1

        # Check if 20 lines have been read
        if line_count == 40:
            break

# The file is automatically closed when exiting the 'with' block