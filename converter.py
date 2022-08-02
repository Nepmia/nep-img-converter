from operator import ne
import sys
import argparse
import os
import logging as log
from PIL import Image

from helpers import list_checker, verify_logs, create_log_folder, log_base_dir, basic_answers, basic_yes_default, user_prompt, parser

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


def convert_images(path_to_exec:str, source_extension:str or list, target_extension:str or list, overwrite:bool):
    
    # Define empty file list
    file_list = []
    
    # Try to list the given path, return a filenotfound if it fails
    log.info("Trying to list given directory.")
    try:
        file_list = os.listdir(path_to_exec)
    except FileNotFoundError:
        log.critical("FileNotFoundError, verify the given path.")
        sys.exit()
    
    log.info("Folder listed, converting images.")
    for file in file_list:
        log.info(f"Converting {file}")
        for extension in source_extension:
            raw_file_name = file.replace(f'.{extension}', '')
            if file.endswith(extension):
                
                for new_extension in target_extension:
                
                    # Defaults to true and will change with prompt
                    answer = True
                
                    if f"{raw_file_name}.{new_extension}" in file_list and not overwrite:
                        answer = user_prompt(basic_answers, f"File {raw_file_name}.{new_extension} already exist, overwrite?", basic_yes_default, "yes")

                    if answer:
                        log.info(f"Converting {file} to {raw_file_name}.{new_extension}")
                        image = Image.open(os.path.join(path_to_exec, file))

                        if new_extension == "jpg" or "jpeg":
                            log.warning("User is converting in jpeg, converting RGBA to RGB.")
                            image = image.convert("RGB")

                        image.save(f"{path_to_exec}/{raw_file_name}.{new_extension}")
                    else:
                        log.warning(f"User denied overwriting of file {raw_file_name}.{new_extension}, skipping it.")

                
    log.info("Job finished.")

if __name__ == "__main__":
    # Define basic args
    parser.add_argument("path_to_exec", help="Path to the folder that contains the image we want to convert")
    parser.add_argument("-s", "--source-extensions", nargs="*", help="List of extensions that needs to be converted (can be single)")
    parser.add_argument("-t", "--target-extensions", nargs="*", help="List of extensions for the newly created files (can be single)")
    parser.add_argument("-o","--overwrite", required=False, default=False, help="Option to always overwrite files", action="store_true")
    parser.add_argument("-c", "--case", required=False, default="snake", help="Option to select export casing, default is snake case. Supports: camel, snake, kebab, pascal")
    
    # Parse the args
    args = parser.parse_args()

    log.info("Starting process.")
    log.debug(f"got args: {args}")

    if args.overwrite:
        log.warn("Overwriting automatically.")

    log.info(args.source_extensions)
    # Launch the conversion
    convert_images(args.path_to_exec, args.source_extensions, args.target_extensions, args.overwrite)

