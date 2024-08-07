import re
import sys
import codecs

def remove_non_latin_extended_chars(text):
    # Define the pattern to match only allowed characters
    # This includes basic Latin letters, Latin Extended characters, spaces, and common punctuation marks
    #pattern = re.compile(r'''[^0-9A-Za-z\u00C0-\u00FF\u0100-\u024F\u1E00-\u1EFF\uA720-\uA7FF\s.,:;!?'"“”‘’«»()\-@#\$%\^&\*\+\/\\_\|~<>{}\[\]=]''', re.VERBOSE)
    pattern = re.compile(r'''[^0-9\s.,:;!?'"“”‘’«»()\-@#\$%\^&\*\+\/\\_\|~<>{}\[\]=]\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF\uAB30-\uAB6F''', re.VERBOSE)
    cleaned_text = pattern.sub('', text)
    return cleaned_text

fentrada=sys.argv[1]
fsortida=sys.argv[2]

entrada=codecs.open(fentrada,"r",encoding="utf-8")
sortida=codecs.open(fsortida,"w",encoding="utf-8")

for linia in entrada:
    linia=linia.rstrip()
    liniamod=remove_non_latin_extended_chars(linia)
    sortida.write(liniamod+"\n")
