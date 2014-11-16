
import urllib2

from tempfile import NamedTemporaryFile 

def write_pdf_data(pdf_data):
	'''Writes a stream of pdf data out to the temporary file system'''

	tf = NamedTemporaryFile(delete=False, suffix=".pdf")
	tf.write(pdf_data)
	tf.close()

	return tf.name

def download_pdf(url):
	'''Downloads a pdf from the supplied url and writes it into a temp file'''

	req = urllib2.Request(url)
	rpdf = urllib2.urlopen(req)
	tf = NamedTemporaryFile(delete=False, suffix=".pdf")
	tf.write(rpdf.read())
	tf.close()

	return tf.name

