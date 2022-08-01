import sys
import os
from PIL import Image

def convert_images(path_to_exec:str, extension_to_convert:str):
    
    file_list = None
    
    try:
        file_list = os.listdir(path_to_exec)
    except FileNotFoundError:
        FileNotFoundError("Unable to find given path, verify that it's correct")
        exit()
    
    if file_list:
        for file in file_list:
            if file.endswith(extension_to_convert):
                image = Image.open(os.path.join(path_to_exec, file))
                image.save(f"{path_to_exec}/{file.replace(f'.{extension_to_convert}', '')}.webp")
                
    print("job suceeded")


if __name__ == "__main__":
    path_to_exec = str(sys.argv[1])
    extension_to_convert = str(sys.argv[2])
    convert_images(path_to_exec, extension_to_convert)

