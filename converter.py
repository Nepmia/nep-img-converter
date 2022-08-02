from operator import ne
import sys
import argparse
import os
import logging as log
from PIL import Image
import humps

from helpers import verify_logs, create_log_folder, log_base_dir, basic_answers, basic_yes_default, user_prompt, parser, allowed_cases

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


def convert_images(path_to_exec:str, source_extension:list, target_extension:list, ignore_names: list, case:str, overwrite:bool):
    
    # Define empty file list
    file_list = []
    
    # Check if the case arg is correct
    if allowed_cases.get(case):
        log.info(f"Exported files will be in {case} case")
    else:
        log.critical("Invalid case name, killing.")
        sys.exit()

    # Try to list the given path, return a filenotfound if it fails
    log.info("Trying to list given directory.")
    try:
        file_list = os.listdir(path_to_exec)
    except FileNotFoundError:
        log.critical("FileNotFoundError, verify the given path.")
        sys.exit()
    
    log.info("Folder listed, converting images.")
    for file in file_list:

        for extension in source_extension:

            raw_file_name = file.replace(f'.{extension}', '')

            # Check if file should be ignored
            if raw_file_name in ignore_names:
                log.warning(f"File {file} is in ignore list, skipping.")
            
            else:
                # Create the correct name for the exported file
                parsed_file_name = eval(f"humps.{allowed_cases[case]}('{raw_file_name}')")
                

                if file.endswith(extension):
                    
                    for new_extension in target_extension:
                    
                        # Defaults to true and will change with prompt
                        answer = True
                    
                        # If the file already exist and if no overwrite rule has
                        # Been set, ask the user if they want to overwrite
                        if f"{parsed_file_name}.{new_extension}" in file_list and not overwrite:
                            answer = user_prompt(
                                basic_answers, 
                                f"File {parsed_file_name}.{new_extension} already exist, overwrite?", 
                                basic_yes_default,
                                "yes"
                            )

                        if answer:

                            log.info(f"Converting {file} to {parsed_file_name}.{new_extension}")
                            image = Image.open(os.path.join(path_to_exec, file))

                            # Special case of jpeg...
                            if "jpg" in new_extension or "jpeg" in new_extension:
                                log.warning("User is converting in jpeg, converting RGBA to RGB.")
                                image = image.convert("RGB")

                            image.save(f"{path_to_exec}/{parsed_file_name}.{new_extension}")
                        else:
                            log.warning(f"User denied overwriting of file {parsed_file_name}.{new_extension}, skipping it.")

                
    log.info("Job finished.")

if __name__ == "__main__":
    # Define basic args
    parser.add_argument("path_to_exec", help="Path to the folder that contains all the images we want to convert")
    parser.add_argument("-s", "--source-extensions", nargs="*", help="List of extensions that needs to be converted (can be single)")
    parser.add_argument("-t", "--target-extensions", nargs="*", help="List of extensions for the newly created files (can be single)")
    parser.add_argument("-i", "--ignore-names", nargs="*", required=False, default=[], help="List of file names that should be ignored (can be single and must be exact without extension)")
    parser.add_argument("-c", "--case", required=False, default="snake", help="Option to select export casing, default is snake case. Supports: camel, snake, kebab, pascal")
    parser.add_argument("-o","--overwrite", required=False, default=False, help="Option to always overwrite files", action="store_true")
    
    # Parse the args
    args = parser.parse_args()

    log.info("Starting process.")
    log.debug(f"got args: {args}")

    if args.overwrite:
        log.warn("Overwriting automatically.")

    # Launch the conversion
    convert_images(
        args.path_to_exec, 
        args.source_extensions, 
        args.target_extensions, 
        args.ignore_names,
        args.case, 
        args.overwrite
    )

