import re
from dateutil.parser import parse, ParserError
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError


formats = [
    '\d+[\/-]\d+[\/-]\d{2}(?:\d{2})?',
    '\d{1}(?:\d{1})\s[a-zA-Z]{3}(?:[a-zA-Z]*)\s\d{2}(?:\d{2})'
]


class ReadError(Exception):
    def __init__(self, filename):
        self.message = "Unable to read PDF"


def read_file(current_pdf):
    try:
        reader = PdfReader(current_pdf)
    except EmptyFileError:
        raise ReadError(current_pdf.filename)

    pages = []
    for page in reader.pages:
        pages.append(page.extractText())

    text = ''.join(pages)
    return text


def find_dates(contents):
    matches = []
    count = 0
    for format in formats:
        # matches += re.findall(format, text)
        m = re.finditer(format, contents)
        for obj in m:
            try:
                current = str(parse(obj.group()).date())
            except:
                continue
            start, end = obj.span()
            extra_chars = 30
            blurb = contents[max(start - extra_chars, 0):min(end + extra_chars, len(contents))]
            blurb = blurb.replace(u'\xa0', u' ')
            blurb = "..." + blurb.replace('\n', ' ') + "..."
            date = {
                "date": current,
                "span": obj.span(),
                "blurb": blurb
            }
            matches.append(date)
        print(matches)
    return {"count": len(matches), "results": matches, "error": False}


def parsePDF(file):
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
