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

reader = PdfReader("../data/57e67bb2-9e60-4905-a9e5-dc68c5cfdc22/ada_1pg.pdf")
pages = []
for page in reader.pages:
    pages.append(page.extractText())

text = ''.join(pages)

matches = []
for format in formats:
    matches += re.findall(format, text)

parsed = []
for date in matches:
    # current = datetime.strptime(date, '%Y-%m-%d')
    try:
        current = str(parse(date).date())
        parsed.append(current)
    except:
        pass

print(parsed)
