
import sys, os, json
from PIL import Image

ALGS = {
    "NEAREST" : Image.NEAREST,
    "BILINEAR" : Image.BILINEAR,
    "BICUBIC" : Image.BICUBIC,
    "LANCZOS" : Image.LANCZOS
}
    
if len(sys.argv) < 2:
    print("you have to drag the files on silly")
    input()
else:
    try:
        with open("webcomicUtilitySettings.json") as settings_file:
            settings = json.loads(settings_file.read())
    except FileNotFoundError:
        print("could not find webcomicUtilitySettings.json")
        input("press enter to close this window")
        quit()
    for fileName in sys.argv[1:]:
        try:
            print("opening %s"%fileName)
            input_image = Image.open(fileName)
            name = os.path.splitext(os.path.split(fileName)[1])[0]
        except IOError:
            print("there was an error opening this file: %s" % fileName)
            continue
        for form in settings["formats"]:
            scale = form["width"]/float(input_image.width)
            print("resizing ... ", end="")
            img = input_image.resize( (int(input_image.width*scale),
                                           int(input_image.height*scale)),
                                          resample=ALGS[form["filter"]] )
            img = img.convert("RGB")
            saveName = "%s.%s"%(name, form["extention"])
            img.save(os.path.join(form["path"],saveName), quality=100)
            print("saved with the %s format"%form["name"])
            
            
        
