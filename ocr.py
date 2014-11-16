
import sys
import pyocr
import pyocr.builders

from PIL import Image

def build_config_info():
	'''Builds configuration information about installed OCR software'''

	tools = pyocr.get_available_tools()
	infos = [{'name': tool.get_name(), 'langs': tool.get_available_languages()} for tool in tools]

	return infos

def get_named_ocr_tool(toolname):
	'''For a given tool name, this function will return an ocr tool'''
	tools = pyocr.get_available_tools()

	for tool in tools:
		if tool.get_name() == toolname:
			return tool

	return None

def img_to_str(img_file, toolname='Tesseract', lang='eng'):
	'''Takes a ras file on disk as input with an ocr tool name and language and provides the full page of text in return'''
	tool = get_named_ocr_tool(toolname)
	return tool.image_to_string(Image.open(img_file), lang=lang, builder=pyocr.builders.TextBuilder())

def img_to_wordbox(img_file, toolname='Tesseract', lang='eng'):
	'''Takes a ras file on disk as input with an ocr tool name and language and provides word boxes in return'''
	tool = get_named_ocr_tool(toolname)
	boxes = tool.image_to_string(Image.open(img_file), lang=lang, builder=pyocr.builders.WordBoxBuilder())

	return [{ 'word': b.content, 'x1': b.position[0][0], 'y1': b.position[0][1], 'x2': b.position[1][0], 'y2': b.position[1][1] } for b in boxes]

def img_to_linebox(img_file, toolname='Tesseract', lang='eng'):
	'''Takes a ras file on disk as input with an ocr tool name and language and provides line boxes in return'''
	tool = get_named_ocr_tool(toolname)
	boxes = tool.image_to_string(Image.open(img_file), lang=lang, builder=pyocr.builders.LineBoxBuilder())

	return [{ 'line': b.content, 'x1': b.position[0][0], 'y1': b.position[0][1], 'x2': b.position[1][0], 'y2': b.position[1][1] } for b in boxes]


