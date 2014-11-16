# ocr

A microservice to provide OCR to larger applications.

## Operating system packages

The following packages are needed on a debian system for this service to operate correctly:

{% highlight bash %}
sudo apt-get install easy_install python-setuptools python-dev libgraphicsmagick++1-dev libboost-python-dev build-tools tesseract-ocr tesseract-ocr-eng libtiff4-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms-dev libwebp-dev python-pythonmagick python-pdfminer libmagickwand-dev imagemagick
{% endhighlight %}