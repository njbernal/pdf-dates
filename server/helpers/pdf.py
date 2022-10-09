import re
from werkzeug.datastructures import FileStorage
from dateutil.parser import parse, ParserError
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError


formats = [
    '\d+[\/-]\d+[\/-]\d{2}(?:\d{2})?',
    '\d{1}(?:\d{1})\s[a-zA-Z]{3}(?:[a-zA-Z]*)\s\d{2}(?:\d{2})',
]


class ReadError(Exception):
    def __init__(self, filename):
        self.message = "Unable to read PDF"


def read_file(current_pdf: FileStorage) -> str:
    try:
        reader = PdfReader(current_pdf)
        # TODO: Check if we need to parse fields or flatten the PDF
        # TODO: This would be useful if so: https://stackoverflow.com/questions/27023043/generate-flattened-pdf-with-python
        # fields = reader.get_fields(current_pdf)
        # field_str = ''
        # for key in fields:
        #     if (fields[key].value):
        #         field_str += fields[key].value + ' '
    except EmptyFileError:
        raise ReadError(current_pdf.filename)

    pages = []
    for page in reader.pages:
        pages.append(page.extractText())

    text = ''.join(pages)
    return text


def find_dates(contents: str) -> object:
    matches = []
    count = 0
    for format in formats:
        regex_matches = re.finditer(format, contents)
        for obj in regex_matches:
            try:
                current = str(parse(obj.group()).date())
            except:
                continue

            # Generate surrounding blurb and clean up the string
            start, end = obj.span()
            extra_chars = 30
            blurb = contents[max(start - extra_chars, 0):min(end + extra_chars, len(contents))]
            blurb = blurb.replace(u'\xa0', u' ')
            blurb = "..." + blurb.replace('\n', ' ') + "..."

            # Returning an object containing the date, where this text is
            # (character indices), and the surrounding blurb
            date = {
                "date": current,
                "span": obj.span(),
                "blurb": blurb
            }
            matches.append(date)
    return {"count": len(matches), "results": matches, "error": False}


def parsePDF(file: FileStorage) -> object:
    """ 
    Parse a PDF using PyPDF library and extract the dates
    :param file: The PDF file to parse
    :return: Object containing 'count', 'results' and 'error'
    """
    # Default object structure
    result = {
        "count": 0,
        "results": [],
        "error": True
    }

    # Attempt to read PDF and extract dates
    # ReadError will be raised if PDF is invalid.
    try:
        contents = read_file(file)
        result = find_dates(contents)
    except ReadError as error:
        result["message"] = error.message
    return result
