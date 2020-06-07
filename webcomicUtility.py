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
		print("img.height: %s" % img.height)

		if form["height"] < img.height:
			crop_index = 1
			for crop_y in range(0, img.height, form["height"]):
				print("cropping ... ", end="")
				if crop_y + form["height"] < img.height:
					crop_height = form["height"]
				else:
					crop_height = img.height - crop_y
				cropped_image = img.crop((0, crop_y, img.width, crop_y + crop_height))

				print("saving ... ", end="")
				save_name = "%s(%d).%s" % (name, crop_index, form["extension"])
				cropped_image.convert("RGB").save(os.path.join(form["path"], save_name), quality=100)
				crop_index += 1
		else:
			print("saving ... ", end="")
			save_name = "%s.%s" % (name, form["extension"])
			img.convert("RGB").save(os.path.join(form["path"], save_name), quality=100)

		print("finished with format %s" % form["name"])
		
