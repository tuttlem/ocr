
import pgmagick
import pgmagick.api

from tempfile import NamedTemporaryFile 
from pyPdf import PdfFileReader

def count_pdf_pages(pdf_file):
	'''Given a pdf file location, this function will count the number of pages within'''

	pdf = PdfFileReader(open(pdf_file, 'rb'))
	return pdf.getNumPages()

def pdf_page_to_img(pdf_file, page,  out_type='.tiff'):
	'''Converts a page inside a PDF file on disk to a image file on disk and returns the image filename'''

	buf = pgmagick.Image(pdf_file + ('[%s]' % page))
	tf = NamedTemporaryFile(delete=False, suffix=out_type)

	#buf.density(pgmagick.Geometry(300, 300))
	buf.quality(100)
	buf.filterType(pgmagick.FilterTypes.SincFilter)
	buf.density('1600x1600')
	buf.sharpen(1.0)

	buf.write(tf.name)
	tf.close()

	return tf.name

def pdf_to_imgs(pdf_file):
	'''Converts an entire PDF to a collection of images. The image file names are returned as an array'''

	count = count_pdf_pages(pdf_file)
	return [pdf_page_to_img(pdf_file, idx) for idx in range(count)]

