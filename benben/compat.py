try:
    unicode
except NameError:
    unicode = str

try:
    basestring
except NameError:
    basestring = str
