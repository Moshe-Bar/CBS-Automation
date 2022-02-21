import sys

import pdfkit

from CbsObjects.Error import Error
from CbsObjects.TestDetails import TestDetails

ROOT_PATH = sys.path[1]
PDF_PATH = ROOT_PATH + '\\Resources\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
PDF_CONFIG = pdfkit.configuration(wkhtmltopdf=PDF_PATH)
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
'''


class Converter:
    @classmethod
    def short_error_to_str(cls, error: Error):

        e_index = error.index
        e_type = error.type
        e_web_part = error.wp_type
        res = None

    @classmethod
    def errors_to_pdf(cls, errors: [], test_details: TestDetails):
        t = test_details
        if not errors:
            return None
        data = TEMPLATE + '''<p class="Title">
                                Test started on: {}<br>
                                Test ended on: {}<br>
                                Candidates: {}<br>
                                Scanned pages: {}<br>
                                Test ID: {}<br></p>'''.format(t.start_date_str(), t.end_date_str(), len(t.candidates()), len(t.scanned()), t.ID())
        groups = errors.sort(key=lambda x:x[1])
        for error in errors:
            data =

        data = data + "</body></html>"
        data = pdfkit.from_string(data, configuration=PDF_CONFIG)

    @classmethod
    def errors_to_excel(cls, errors: []):
        pass
