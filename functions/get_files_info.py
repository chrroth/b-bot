import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    #print (f"working_dir_abs = {working_dir_abs}")
    #print (f"target_dir = {target_dir}")
    #print (f"valid_target_dir = {valid_target_dir}")

    if not valid_target_dir:
        return print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.isdir(target_dir):
        return print(f'Error: "{directory}" is not a directory')
    
    
    
    contents = os.listdir(target_dir)

    #print (contents)

    string = ""

    for item in contents:
        name = item

        try:
            size = os.path.getsize(target_dir + "/" + item)
        except Exception as e:
            return print(f"Error: {e}")
        
        try:
            is_dir = os.path.isdir(target_dir + "/" + item)
        except Exception as e:
            return print(f"Error: {e}")
        
        string += "- " + name + ": file_size=" + str(size) + " bytes, is_dir=" + str(is_dir) + "\n"

        #print (string)

    return print(string)

    