import re
from werkzeug.datastructures import FileStorage
from dateutil.parser import parse
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError

"""
DateExtractor class and related error
Purpose:    To extract dates from a PDF file and return matches as 
            a JSON object.
"""


class ReadError(Exception):
    """
    A Custom error to use with DateExtractor when reading
    a PDF file fails.
    """

    def __init__(self, filename=""):
        self.message = "Unable to read PDF."
        self.filename = filename


class DateExtractor:
    """
    A class that uses PdfReader from PyPDF2 to extract
    dates from a PDF file.
    Currently checks text and form fields.
    In the future, could add annotations, or other PDF 
    options to be researched.
    """

    def __init__(self, pdf_object: FileStorage) -> None:
        self._formats = [
            '\d+[\/-]\d+[\/-]\d{2}(?:\d{2})?',
            '\d{1}(?:\d{1})\s[a-zA-Z]{3}(?:[a-zA-Z]*)\s\d{2}(?:\d{2})',
            '\d{1}(?:\d{1})[\s\/]\d{1}(?:\d{1})[\s]\d{2}(?:\d{2})',
            '[a-zA-Z]+\s\d{1}(?:\d{1})?[\s\,]?\s\d{2}(?:\d{2})?',
            '\d{1}(?:\d{1})[thsnd]*\sday\sof\s[a-zA-Z]{3}(?:[a-zA-Z]*)\,?\s\d{2}(?:\d{2})'
        ]
        self._pdf_object = pdf_object
        self._filename = pdf_object.filename
        self._reader = self.init_reader()
        self._text_matches = self.extract_from_text()
        self._field_matches = self.extract_from_fields()
        self._results = self.generate_result()

    def init_reader(self) -> PdfReader:
        """
        Initialize PDF reader from PyPDF2 and pass it the current file.
        :return: The PdfReader object
        """
        try:
            reader = PdfReader(self._pdf_object)
        except EmptyFileError:
            raise ReadError(self._filename)
        return reader

    def get_results(self) -> object:
        """ Getter for match results """
        return self._results

    def extract_from_text(self) -> object:
        """
        Extract date matches from text blurb.
        :return: matches in JSON object
        """
        pages = []
        for page in self._reader.pages:
            pages.append(page.extractText())
        text = ''.join(pages)
        return self.find_text_matches(text)

    def extract_from_fields(self) -> object:
        """
        Extract non-empty form fields into an object
        for further processing.
        :return: matches in JSON object 
        """
        non_empty_fields = []
        try:
            fields = self._reader.get_fields()
        except:
            raise ReadError(self._filename)
        if not fields:
            return {"count": 0, "results": []}
        for key in fields:
            if (fields[key].value is not None):
                non_empty_fields.append(str(fields[key].value))

        return self.find_field_matches(non_empty_fields)

    def find_field_matches(self, fields: list) -> object:
        """
        Finds date matches in PDF fields
        :return: matches in JSON format
        """
        matches = []
        for field in fields:
            for format in self._formats:
                regex_matches = re.finditer(format, field)
                # Attempt to parse match into a date for confirmation
                for obj in regex_matches:
                    try:
                        current = str(parse(obj.group()).date())
                    except:
                        continue
                    blurb = "..." + field + " (in form field)..."
                    date = {
                        "date": current,
                        "span": obj.span(),
                        "blurb": blurb
                    }
                    matches.append(date)
        return {"count": len(matches), "results": matches}

    def find_text_matches(self, contents: str) -> object:
        """
        Uses regex formats to match dates in text
        :param contents: A string to parse for date matches
        :return: matches in JSON format
        """
        matches = []
        for format in self._formats:
            regex_matches = re.finditer(format, contents)
            for obj in regex_matches:
                # Attempt to parse match into a date for confirmation
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
        return {"count": len(matches), "results": matches}

    def generate_result(self) -> object:
        """
        Combine results of all match types.
        :return: JSON matches
        """
        text = self._text_matches
        fields = self._field_matches
        results = text['results'] + fields['results']
        results = sorted(results, key=lambda x: x['date'])

        return {
            "count": text['count'] + fields['count'],
            "results": results
        }
