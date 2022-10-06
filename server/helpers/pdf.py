from dateutil.parser import parse, ParserError
from dateutil.tz import tzutc
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError


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
        pages.append(page.extractText().split('\n'))
    return pages


def find_dates(contents):
    file_results, count = [], 0
    for page in contents:
        page_results = []
        for line in page:
            try:
                dates = parse(line, tzinfos={'FOX': tzutc()}, fuzzy=True)
                date_str = str(dates.date())
                page_results.append((date_str, line))
            except ParserError:
                pass

        # Increase date count and append results to file_results
        count += len(page_results)
        file_results.append(page_results)

    return {"count": count, "results": file_results, "error": False}


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
