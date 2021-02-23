#!/usr/bin/python3

import sys, os, json
from PIL import Image

ALGS = {
    "NEAREST"  : Image.NEAREST,
    "BILINEAR" : Image.BILINEAR,
    "BICUBIC"  : Image.BICUBIC,
    "LANCZOS"  : Image.LANCZOS
}
    
if len(sys.argv) < 2:
    print("no files specified")
    quit()

try:
    with open("webcomicUtilitySettings.json") as settings_file:
        settings = json.loads(settings_file.read())
except FileNotFoundError:
    print("could not find webcomicUtilitySettings.json")
    quit()

for file_name in sys.argv[1:]:
    try:
        print("opening %s" % file_name)
        input_image = Image.open(file_name)
        name = os.path.splitext(os.path.split(file_name)[1])[0]
    except IOError:
        print("failed to open %s" % file_name)
        continue

    for form in settings["formats"]:
        print("\tresizing for %s" % form["name"])
        scale = form["width"] / float(input_image.width)
        img = input_image.resize(
            ( int(input_image.width * scale), int(input_image.height * scale) ),
            resample=ALGS[form["filter"]]
        )

        if form["height"] < img.height:
            crop_index = 1
            for crop_y in range(0, img.height, form["height"]):
                if crop_y + form["height"] < img.height:
                    crop_height = form["height"]
                else:
                    crop_height = img.height - crop_y
                cropped_image = img.crop((0, crop_y, img.width, crop_y + crop_height))

                save_name = "%s(%d).%s" % (name, crop_index, form["extension"])
                print("\t\tcropping and saving to %s" % save_name)
                cropped_image.convert("RGB").save(os.path.join(form["path"], save_name), quality=100)
                crop_index += 1
        else:
            save_name = "%s.%s" % (name, form["extension"])
            print("\t\tsaving to %s" % save_name)
            img.convert("RGB").save(os.path.join(form["path"], save_name), quality=100)
        
