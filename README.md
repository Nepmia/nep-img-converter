# PILLOW Image converter
This script uses pillow to convert all images in a single folder, I'll maybe add recursive support for subfolders at somepoint but I don't need it for now.

The script is able to convert multiple souce extensions to multiple extensions, it also allow you to chose casing of the export, default is snake case. 

You can also provide a list of ignores names so the script don't convert those images.

## Setup

In order to use the script you must setup the `LOG_BASE_DIR`, which will be the folder where the script will output its logging 

you can disable loging in a file by commenting / deleting the `FileHandler` at line 20 :

    log.FileHandler(f"{log_base_dir}/converter.log")

(can also rename the output file there)

## Usage

    converter.py [-h] [-s [SOURCE_EXTENSIONS ...]] [-t [TARGET_EXTENSIONS ...]] [-i [IGNORE_NAMES ...]] [-c CASE] [-o] path_to_exec

You can view all possibilities and options using 
`converter.py -h`


But globally it's kinda easy to use:

    python converter.py "path/to/the/folder" -s "png" "jpg" -t "webp" -o -i "mycat" -c "camel"

This will convert all `.png` and `.jpg` files in `path/to/the/folder` to `.webp` overwriting possibly existing `.webp` with the same name, it will export the new files in camelCase and ignore the image named "mycat" no matter its extension.

We could have used unshortcuted options as such but it's longer:

    python converter.py "path/to/the/folder" --source-extensions "png" "jpg" --target-extensions "webp" --overwrite --ignore-names "mycat" --case "camel"

## Logging

The script use the default logging lib from Python, it logs all levels from debug to critical, you can change the level of logging at line 16 or add new logs using `log.level(message)`