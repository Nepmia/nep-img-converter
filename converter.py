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


def convert_images(path_to_exec:str, source_extension:str, target_extension:str):
    
    file_list = None
    
    log.info("Trying to list given directory.")
    try:
        file_list = os.listdir(path_to_exec)
    except FileNotFoundError:
        log.critical("FileNotFoundError, verify the given path.")
        exit()
    

    if file_list:
        log.info("Folder listed, converting images.")
        for file in file_list:
            if file.endswith(source_extention):
                log.info(f"Converting {file} to {file}.{target_extension}")
                image = Image.open(os.path.join(path_to_exec, file))
                image.save(f"{path_to_exec}/{file.replace(f'.{source_extention}', f'.{target_extension}')}")
                
    log.info("Process finished without returning errors.")


if __name__ == "__main__":
    path_to_exec = str(sys.argv[1])
    source_extention = str(sys.argv[2])
    target_extention = str(sys.argv[2])
    log.info("Starting process.")
    convert_images(path_to_exec, source_extention, target_extention)

