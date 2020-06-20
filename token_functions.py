import os
import re

def parse_token(file_string_to_parse, token_regex_format):
    '''
    This functions takes an input tokenized string, and returns a dictionary with 
    the token information. This information can be used to extract the fields needed 
    to build a directory structure from the tokenized string.
    
    The main key of the dictionary is the token order.
    
    This fuction makes extensive use of this: https://docs.python.org/3/library/re.html#match-objects
    '''
    # Create list to hold token info
    token_dict = {}
    
    '''Tracker to replace tokens with their length in ?'s
            This is to ensure the token start position is in the correct place
            On the second loop iteration file_sample_{1:5}_{2:3} will look like file_sample_?????_{2:3}
            to ensure the second token starts in the correct position
    '''
    format_start_tracker = file_string_to_parse

    # Find all tokens in the string
    for match in re.finditer(token_regex_format, file_string_to_parse): 
        #Get the token text
        token_text = match.group(0)
    
        # Parse token text to get token order number
            # This will determine the order the final directories are created in
        token_number = token_text[1:token_text.find(':')]
    
        # Parse token text to get token length
        token_length = token_text[(token_text.find(':')+1):-1]
    
        # Get where the token starts in the filename string
        token_start_position = format_start_tracker.find(token_text)
    
        # Build the output dictionary 
        output_dic = {int(token_number): {
                      'token_length': int(token_length),
                      'token_start_position' : int(token_start_position),
                      'token_text' : token_text}}
    
        # Append to the main list
        token_dict.update(output_dic)
        
        # Replace token with number of characters from the length to get correct
        # starting position in next loop
        format_start_tracker = re.sub(token_text, '?'*int(token_length), format_start_tracker)
    
    return token_dict
    
    
  
def move_tokenized_file(source_root, destination_root, file_name, token_dict):
    '''
    This function moves an input file to a destination file path based on 
    a tokenized file name.
    
    source_root: where the file is currently located
    
    destination_root: the root directory that all new directories will be created under
        --if destination_root is an empty string, it will default to the source_root
    
    file_name: the input file name
    
    token_dict: a dictionary containing token information to parse the file name
        --this dictionary is created using the parse_token function
    '''
    # Combine source with file name
    source_path = os.path.join(source_root, file_name)
    
    # Assign a destination path if provided, otherwise default to source
    if destination_root == '':
        destination_path = source_root
    else:
        destination_path = destination_root

    # Loop through the dictionary and add each token to the destination path
    for key in token_dict:
        # Get where to start/end the slice of the string
        slice_start = token_dict[key]['token_start_position']
        slice_end = slice_start + token_dict[key]['token_length']

        # Add slice to path
        destination_path = os.path.join(destination_path, file_name[slice_start:slice_end])
        
    # Add the filename to the end of the path
    destination_path = os.path.join(destination_path, file_name)
    
    # Perform the file move
        # The renames function creates all intermediate directories needed
    os.renames(source_path, destination_path)