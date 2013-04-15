try:
    unicode = unicode
except NameError:
    unicode = str

try:
    basestring = basestring
except NameError:
    basestring = str
