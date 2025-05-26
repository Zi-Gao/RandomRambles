input_text = """
"""

# Split the input text into lines
lines = input_text.strip().split('\n')

# Process each line and create the output format

mp={}

output_lines = []
for line in lines:
    parts = line.split('\t')
    # print(parts)
    
    # Check if the line has enough parts (at least 3)
    if len(parts) >= 3: 
        platform = parts[-2].split()[0]  # Get the platform (QOJ or AtCoder)
        problem_id = parts[-2].split()[1]  # Get the problem ID
        
        if (platform,problem_id) in mp:
            continue
        mp[(platform,problem_id)]=1

        # Always consider the problem as solved ('1')
        output_line = f"{platform}\t|\t{problem_id}\t|\t1\t|"
        output_lines.append(output_line)



# Join the output lines
output_text = '\n'.join(output_lines)

# Print the output text
print(output_text)