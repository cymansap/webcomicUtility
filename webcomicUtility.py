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
		print("resizing ... ", end="")
		scale = form["width"] / float(input_image.width)
		img = input_image.resize(
			( int(input_image.width * scale), int(input_image.height * scale) ),
			resample=ALGS[form["filter"]]
		)

		print("saving ... ", end="")
		img = img.convert("RGB")
		save_name = "%s.%s" % (name, form["extension"])
		img.save(os.path.join(form["path"], save_name), quality=100)

		print("finished with format %s" % form["name"])
		
