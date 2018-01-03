try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import re

def get_num_from_screenshot(path):
	result = pytesseract.image_to_string(Image.open(path))
	print result
	try:
		if result and type(result) == type(""):
			result = re.findall('\+?[91]{2}?[789][0-9]{9}', result)
		else:
			result = 0
			print "Failed parsing" + str(result)
	except:
		result = 0
		print "Failed parsing " + str(result)
