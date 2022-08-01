import sys
import os
import logging as log
from PIL import Image

from helpers import verify_logs, create_log_folder, log_base_dir

if not verify_logs():
    create_log_folder()

log.basicConfig(
    encoding="utf-8",
    level=log.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log.FileHandler(f"{log_base_dir}/converter.log"),
        log.StreamHandler(sys.stdout),
    ],
    datefmt="%Y-%m-%d %H:%M:%S",
)


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

