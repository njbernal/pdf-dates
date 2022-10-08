import re
from PyPDF2 import PdfReader
from PyPDF2.errors import EmptyFileError
from datetime import datetime
from dateutil.parser import parse, ParserError
from dateutil.tz import tzutc

formats = [
    '\d+[\/-]\d+[\/-]\d{2}(?:\d{2})?',
    '\d{1}(?:\d{1})\s[a-zA-Z]{3}(?:[a-zA-Z]*)\s\d{2}(?:\d{2})'
]


def make_blurb(span, text):
    extra = 30
    start, end = span
    sub = text[max(start - extra, 0):min(end + extra, len(text))]
    sub = sub.replace('\n', ' ')
    sub = '...' + sub + '...'
    return sub


reader = PdfReader("../data/57e67bb2-9e60-4905-a9e5-dc68c5cfdc22/ada_1pg.pdf")
pages = []
for page in reader.pages:
    pages.append(page.extractText())

text = ''.join(pages)
matches = []
for format in formats:
    # matches += re.findall(format, text)
    m = re.finditer(format, text)
    for obj in m:
        try:
            current = str(parse(obj.group()).date())
        except:
            continue
        print(obj.group())
        blurb = make_blurb(obj.span(), text)
        date = {
            "date": current,
            "span": obj.span(),
            "blurb": blurb
        }
        matches.append(date)

print(matches)
