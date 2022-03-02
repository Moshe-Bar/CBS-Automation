import sys

import pdfkit


ROOT_PATH = sys.path[1]
path = ROOT_PATH + '\\Resources\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf=path)
pdfkit.from_file('test.html', 'out.pdf',configuration=config)
