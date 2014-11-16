import sys
import os
import base64

import ocr
import ras
import util

from flask import Flask, request
from flask.ext.restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

class Config(Resource):
	'''The Config resource provides OCR system configuration information'''

	def get(self):
		return ocr.build_config_info()

class PageToImage(Resource):
	'''The PageToImage resource provides pdf rasterisation services''' 

	def post(self):
		src = None
		dest = None

		try:
			parser = reqparse.RequestParser()
			parser.add_argument('pdf', type=str)	# pdf byte data
			parser.add_argument('url', type=str)	# url location of the pdf
			parser.add_argument('page', type=int)	# the page number to rasterize
			parser.add_argument('type', type=str)	# the output raster

			args = parser.parse_args()

			pdf = args['pdf']
			url = args['url']
			page = args['page'] or 1
			ras_type = args['type'] or 'tif'

			# get the pdf data on disk
			if pdf != None:
				src = util.write_pdf_data(pdf)
			elif url != None:
				src = util.download_pdf(url)
			else:
				abort(400, message='No pdf data or url was supplied')

			# turn it into raster
			dest = ras.pdf_page_to_img(src, page, '.%s' % ras_type)
			ras_data = None

			# read out the raster data to return
			with open(dest, 'r') as ras_file:
				ras_data = ras_file.read()

			return { 'image': base64.b64encode(ras_data) }
		except Exception, e:
			return { 
				'error': {
					'message': e.message,
					'doc': e.__doc__
				}
			}
		finally:
			# destroy the created files
			if src != None:
				os.unlink(src)

			if dest != None:
				os.unlink(dest)

class PdfToImages(Resource):
	'''The PdfToImages resource provides rasterisation services for whole documents'''

	def post(self):
		src = None
		dests = None

		try:
			parser = reqparse.RequestParser()
			parser.add_argument('pdf', type=str)	# pdf byte data
			parser.add_argument('url', type=str)	# url location of the pdf
			parser.add_argument('type', type=str)	# the output raster

			args = parser.parse_args()

			pdf = args['pdf']
			url = args['url']
			ras_type = args['type'] or 'tif'

			# get the pdf data on disk
			if pdf != None:
				src = util.write_pdf_data(pdf)
			elif url != None:
				src = util.download_pdf(url)
			else:
				abort(400, message='No pdf data or url was supplied')

			# turn it into raster
			dests = ras.pdf_to_imgs(src)
			ras_data = { 'images': [] }

			for dest in dests:
				# read out the raster data to return
				with open(dest, 'r') as ras_file:
					ras_data['images'].append(base64.b64encode(ras_file.read()))

			return ras_data
		except Exception, e:
			return { 
				'error': {
					'message': e.message,
					'doc': e.__doc__
				}
			}
		finally:
			# destroy the created files
			if src != None:
				os.unlink(src)

			if dests != None:
				for dest in dests:
					os.unlink(dest)

class PdfToString(Resource):
	'''Performs an OCR process on a PDF to produce a string per page'''

	def post(self):
		src = None
		dests = None

		try:
			parser = reqparse.RequestParser()
			parser.add_argument('pdf', type=str)	# pdf byte data
			parser.add_argument('url', type=str)	# url location of the pdf
			parser.add_argument('tool', type=str)	# the tool to use
			parser.add_argument('lang', type=str)	# the language to use
			parser.add_argument('mode', type=str)	# the mode of extraction

			args = parser.parse_args()

			pdf = args['pdf']
			url = args['url']
			tool = args['tool'] or 'Tesseract'
			lang = args['lang'] or 'eng'
			mode = args['mode'] or 'text'

			# get the pdf data on disk
			if pdf != None:
				src = util.write_pdf_data(pdf)
			elif url != None:
				src = util.download_pdf(url)
			else:
				abort(400, message='No pdf data or url was supplied')

			# turn it into raster
			dests = ras.pdf_to_imgs(src)
			texts = []

			for dest in dests:
				if mode == 'text':
					texts.append(ocr.img_to_str(dest, tool, lang))
				elif mode == 'word':
					texts.append(ocr.img_to_wordbox(dest, tool, lang))
				elif mode == 'line':
					texts.append(ocr.img_to_linebox(dest, tool, lang))

			return texts
		except Exception, e:
			return { 
				'error': {
					'message': e.message,
					'doc': e.__doc__
				}
			}
		finally:
			# destroy the created files
			if src != None:
				os.unlink(src)

			if dests != None:
				for dest in dests:
					os.unlink(dest)	

# Define all of the application's source routes here
api.add_resource(Config, '/conf')
api.add_resource(PageToImage, '/page2img')
api.add_resource(PdfToImages, '/pdf2imgs')
api.add_resource(PdfToString, '/pdf2str')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)