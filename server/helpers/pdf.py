import re
from werkzeug.datastructures import FileStorage
from dateutil.parser import parse
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError


formats = [
    '\d+[\/-]\d+[\/-]\d{2}(?:\d{2})?',
    '\d{1}(?:\d{1})\s[a-zA-Z]{3}(?:[a-zA-Z]*)\s\d{2}(?:\d{2})',
    '\d{1}(?:\d{1})[\s\/]\d{1}(?:\d{1})[\s]\d{2}(?:\d{2})',
    '[a-zA-Z]+\s\d{1}?[\d]?[\,]?\s?\d{2}(?:\d{2})?'
]


class ReadError(Exception):
    def __init__(self, filename):
        self.message = "Unable to read PDF"


class DateExtractor:
    def __init__(self, pdf_object: FileStorage) -> None:
        self._filename = pdf_object.filename
        self._reader = self.init_reader(pdf_object)
        self._text_matches = self.extract_from_text()
        self._field_matches = self.extract_from_fields()
        self._results = self.generate_result()

    def init_reader(self, pdf_object: FileStorage) -> PdfReader:
        try:
            reader = PdfReader(pdf_object)
        except EmptyFileError:
            raise ReadError(pdf_object.filename)
        return reader

    def get_results(self) -> object:
        return self._results

    def extract_from_text(self) -> object:
        pages = []
        for page in self._reader.pages:
            pages.append(page.extractText())
        text = ''.join(pages)
        return self.find_text_matches(text)

    def extract_from_fields(self) -> object:
        non_empty_fields = []
        fields = self._reader.get_fields()
        if not fields:
            return {"count": 0, "results": []}
        for key in fields:
            if (fields[key].value is not None):
                non_empty_fields.append(str(fields[key].value))

        return self.find_field_matches(non_empty_fields)

    def find_field_matches(self, fields: list) -> object:
        matches = []
        for field in fields:
            for format in formats:
                regex_matches = re.finditer(format, field)
                for obj in regex_matches:
                    try:
                        current = str(parse(obj.group()).date())
                    except:
                        continue
                    start, end = obj.span()
                    blurb = "..." + field + " (in form field)..."
                    date = {
                        "date": current,
                        "span": obj.span(),
                        "blurb": blurb
                    }
                    matches.append(date)
        return {"count": len(matches), "results": matches}

    def generate_result(self) -> object:
        text = self._text_matches
        fields = self._field_matches
        return {
            "count": text['count'] + fields['count'],
            "results": text['results'] + fields['results']
        }

    def find_text_matches(self, contents: str) -> object:
        matches = []
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
                blurb = contents[max(start - extra_chars, 0)
                                     :min(end + extra_chars, len(contents))]
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
