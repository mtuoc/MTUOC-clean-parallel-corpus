#    MTUOC-clean-parallel-corpus
#    Copyright (C) 2024  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import codecs
import re
import sys
from xml.sax.saxutils import unescape
import html
import argparse

#from bs4 import BeautifulSoup
import re
import regex as rx
from ftfy import fix_encoding
import unicodedata

def remove_non_latin_extended_chars(text):
    # Define the pattern to match only allowed characters
    # This includes basic Latin letters, Latin Extended characters, spaces, and common punctuation marks
    #pattern = re.compile(r'''[^0-9A-Za-z\u00C0-\u00FF\u0100-\u024F\u1E00-\u1EFF\uA720-\uA7FF\s.,:;!?'"“”‘’«»()\-@#\$%\^&\*\+\/\\_\|~<>{}\[\]=]''', re.VERBOSE)
    pattern = re.compile(r'''[^0-9\s.,:;!?'"“”‘’«»()\-@#\$%\^&\*\+\/\\_\|~<>{}\[\]=]\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF\uAB30-\uAB6F''', re.VERBOSE)
    cleaned_text = pattern.sub('', text)
    return cleaned_text

def remove_non_unicode_script_chars(text):
    """
    Remove characters that are not in the specified Unicode ranges for all scripts.

    Parameters:
    text (str): The input text to be cleaned.

    Returns:
    str: The cleaned text with only allowed characters.
    """
    # Define the pattern to match only allowed characters from all Unicode scripts
    pattern = re.compile(r'''[^\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F\u0250-\u02AF\u02B0-\u02FF
                             \u0300-\u036F\u0370-\u03FF\u0400-\u04FF\u0500-\u052F\u0530-\u058F\u0590-\u05FF
                             \u0600-\u06FF\u0700-\u074F\u0750-\u077F\u0780-\u07BF\u07C0-\u07FF\u0800-\u083F
                             \u0840-\u085F\u0860-\u086F\u08A0-\u08FF\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F
                             \u0A80-\u0AFF\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F
                             \u0D80-\u0DFF\u0E00-\u0E7F\u0E80-\u0EFF\u0F00-\u0FFF\u1000-\u109F\u10A0-\u10FF
                             \u1100-\u11FF\u1200-\u137F\u1380-\u139F\u13A0-\u13FF\u1400-\u167F\u1680-\u169F
                             \u16A0-\u16FF\u1700-\u171F\u1720-\u173F\u1740-\u175F\u1760-\u177F\u1780-\u17FF
                             \u1800-\u18AF\u18B0-\u18FF\u1900-\u194F\u1950-\u197F\u1980-\u19DF\u19E0-\u19FF
                             \u1A00-\u1A1F\u1A20-\u1AAF\u1AB0-\u1AFF\u1B00-\u1B7F\u1B80-\u1BBF\u1BC0-\u1BFF
                             \u1C00-\u1C4F\u1C50-\u1C7F\u1C80-\u1C8F\u1C90-\u1CBF\u1CC0-\u1CCF\u1CD0-\u1CFF
                             \u1D00-\u1D7F\u1D80-\u1DBF\u1DC0-\u1DFF\u1E00-\u1EFF\u1F00-\u1FFF\u2000-\u206F
                             \u2070-\u209F\u20A0-\u20CF\u20D0-\u20FF\u2100-\u214F\u2150-\u218F\u2190-\u21FF
                             \u2200-\u22FF\u2300-\u23FF\u2400-\u243F\u2440-\u245F\u2460-\u24FF\u2500-\u257F
                             \u2580-\u259F\u25A0-\u25FF\u2600-\u26FF\u2700-\u27BF\u27C0-\u27EF\u27F0-\u27FF
                             \u2800-\u28FF\u2900-\u297F\u2980-\u29FF\u2A00-\u2AFF\u2B00-\u2BFF\u2C00-\u2C5F
                             \u2C60-\u2C7F\u2C80-\u2CFF\u2D00-\u2D2F\u2D30-\u2D7F\u2D80-\u2DDF\u2DE0-\u2DFF
                             \u2E00-\u2E7F\u2E80-\u2EFF\u2F00-\u2FDF\u2FF0-\u2FFF\u3000-\u303F\u3040-\u309F
                             \u30A0-\u30FF\u3100-\u312F\u3130-\u318F\u3190-\u319F\u31A0-\u31BF\u31C0-\u31EF
                             \u31F0-\u31FF\u3200-\u32FF\u3300-\u33FF\u3400-\u4DBF\u4DC0-\u4DFF\u4E00-\u9FFF
                             \uA000-\uA48F\uA490-\uA4CF\uA4D0-\uA4FF\uA500-\uA63F\uA640-\uA69F\uA6A0-\uA6FF
                             \uA700-\uA71F\uA720-\uA7FF\uA800-\uA82F\uA830-\uA83F\uA840-\uA87F\uA880-\uA8DF
                             \uA8E0-\uA8FF\uA900-\uA92F\uA930-\uA95F\uA960-\uA97F\uA980-\uA9DF\uA9E0-\uA9FF
                             \uAA00-\uAA5F\uAA60-\uAA7F\uAA80-\uAADF\uAAE0-\uAAFF\uAB00-\uAB2F\uAB30-\uAB6F
                             \uAB70-\uABBF\uABC0-\uABFF\uAC00-\uD7AF\uD7B0-\uD7FF\uD800-\uDB7F\uDB80-\uDBFF
                             \uDC00-\uDFFF\uE000-\uF8FF\uF900-\uFAFF\uFB00-\uFB4F\uFB50-\uFDFF\uFE00-\uFE0F
                             \uFE10-\uFE1F\uFE20-\uFE2F\uFE30-\uFE4F\uFE50-\uFE6F\uFE70-\uFEFF\uFF00-\uFFEF
                             \uFFF0-\uFFFF]''', re.VERBOSE)

    # Substitute non-matching characters with an empty string
    cleaned_text = pattern.sub('', text)

    return cleaned_text

def remove_tags(segment):
    segmentnotags=re.sub('<[^>]+>',' ',segment).strip()
    segmentnotags=re.sub(' +', ' ', segmentnotags)
    return(segmentnotags)


def normalize_apos(segment):
    segment=segment.replace("’","'")
    segment=segment.replace("`","'")
    segment=segment.replace("‘","'")
    return(segment)
    
def remove_empty(SLsegment,TLsegment):
    remove=False
    if SLsegment.strip()=="": remove=True
    if TLsegment.strip()=="": remove=True
    return(remove)

def remove_short(segment,minimum):
    remove=False
    if len(segment)<int(minimum):
        remove=True
    return(remove)

def remove_equal(SLsegment,TLsegment):
    remove=False
    if SLsegment.strip()==TLsegment.strip(): remove=True
    return(remove)
    
def unescape_html(segment):
    segmentUN=html.unescape(segment)
    return(segmentUN)
    
def percentNUM(segment):
    nl=0
    nn=0
    for l in segment:
        if l.isdigit():
            nn+=1
        else:
            nl+=1
    if len(segment)>0:
        percent=100*nn/len(segment)
    else:
        percent=0
    return percent
def percentLET(segment):
    nl=0
    nn=0
    for l in segment:
        if l.isdigit():
            nn+=1
        else:
            nl+=1
    percent=100*nl/len(segment)
    return percent
    
def percentURLPC(segment):
    lenseg=len(segment)
    urls=findURLs(segment)
    if len(urls)==0:
        percent=0
        return(percent)
    else:
        segmentNOURL=segment
        lenURLs=0
        for url in urls:
            lenURLs+=len(url)
        percent=100*lenURLs/lenseg
        return(percent)
    
def findURLs(text):
    # Regular expression for identifying URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    # Find all matches using the regular expression
    matches = re.findall(url_pattern, text)
    return(matches)
    
def escapeforMoses(segment):
    segment=segment.replace("[","&lbrack;")
    segment=segment.replace("]","&rbrack;")    
    segment=segment.replace("|","&verbar;")
    segment=segment.replace("<","&lt;")
    segment=segment.replace(">","&gt;")
    return(segment)

def remove_control_characters(cadena):
    return rx.sub(r'\p{C}', '', cadena)
    
def is_printable(char):
    category = unicodedata.category(char)
    return not (category.startswith('C') or category in ['Zl', 'Zp', 'Cc'])

def remove_non_printable(string):
    cleaned_string = ''.join(c for c in string if is_printable(c))
    return(cleaned_string)
    
def is_valid_float(s):
    try:
        float(s)
        return(True)
    except ValueError:
        return(False)

parser = argparse.ArgumentParser(description='MTUOC program for cleaning tab separated parallel corpora.')
parser.add_argument('-i','--in', action="store", dest="inputfile", help='The input file.',required=True)
parser.add_argument('-o','--out', action="store", dest="outputfile", help='The output file.',required=True)
parser.add_argument('-a','--all', action="store_true", dest="all", help='Performs default cleaning actions.')
parser.add_argument('--remove_control_characters', action='store_true', default=False, dest='remove_control_characters',help='Remove control characters.')
parser.add_argument('--remove_non_printable', action='store_true', default=False, dest='remove_non_printable',help='Remove control characters.')
parser.add_argument('--norm_apos', action='store_true', default=False, dest='norm_apos',help='Normalize apostrophes.')
parser.add_argument('--norm_unicode', action='store_true', default=False, dest='norm_unicode',help='Normalize unicode characters to NFKC.')
parser.add_argument('--remove_tags', action='store_true', default=False, dest='remove_tags',help='Removes html/XML tags.')
parser.add_argument('--unescape_html', action='store_true', default=False, dest='unescape_html',help='Unescapes html entities.')
parser.add_argument('--fixencoding', action='store_true', default=False, dest='fixencoding',help='Tries to restore errors in encoding.')
parser.add_argument('--remove_empty', action='store_true', default=False, dest='remove_empty',help='Removes segments with empty SL or TL segments.')
parser.add_argument('--remove_short', action='store', default=False, dest='remove_short',help='Removes segments with less than the given number of characters.')
parser.add_argument('--remove_equal', action='store_true', default=False, dest='remove_equal',help='Removes segments with equal SL or TL segments.')
parser.add_argument('--remove_NUMPC', action='store', default=False, dest='remove_NUMPC',help='Removes segments with a percent of numbers higher than the given.')
parser.add_argument('--remove_URLPC', action='store', default=False, dest='remove_URLPC',help='Removes segments with a percent of URLs higher than the given.')
parser.add_argument('--remove_URL', action='store_true', default=False, dest='remove_URL',help='Removes segments with URLs.')
parser.add_argument('--remove_long', action='store', dest='remove_long', type=int, help='Removes segments with more characters than the given number.')
parser.add_argument('--remove_non_latin', action='store_true', default=False, dest='remove_non_latin', help='Removes chars outside the latin extended.')
parser.add_argument('--remove_non_script', action='store_true', default=False, dest='remove_non_script', help='Removes chars outside the Unicode script chars.')
parser.add_argument('--check_weights', action='store_true', dest='check_weights', help='Removes segments not having a valid weight.')

parser.add_argument('--escapeforMoses', action='store_true', default=False, dest='escapeforMoses',help='Replaces [ ] and | with entities.')
parser.add_argument('--stringFromFile', action='store', default=False, dest='stringFromFile',help='Removes segments containing strings from the given file (one string per line).')
parser.add_argument('--regexFromFile', action='store', default=False, dest='regexFromFile',help='Removes segments matching regular expressions from the given file (one regular expression per line).')
parser.add_argument('--vSL', action='store', default=False, dest='vSL',help='Verify language of source language segments.')
parser.add_argument('--vTL', action='store', default=False, dest='vTL',help='Verify language of target language segments.')
parser.add_argument('--vSetLanguages', action='store', default=False, dest='vSetLanguages',help='Set the possible languages (separated by ",". For example: en,es,fr,ru,ar,zh.)')
parser.add_argument('--vTNOTL', action='store', default=False, dest='vTNOTL',help='Verify target language not being a given one (to avoid having SL in TL, for example).')
parser.add_argument('--noUPPER', action='store_true', default=False, dest='noUPPER',help='Deletes the segment if it is uppercased (either source or target segment).')
parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',help='If set, shows the actions on standard output.')

args = parser.parse_args()

if args.all:
    args.remove_control_characters=True
    args.remove_non_printable=True
    #args.norm_apos=True
    args.norm_unicode=True
    args.remove_tags=True
    args.unescape_html=True
    args.fixencoding=True
    args.remove_empty=True
    args.remove_equal=True
    if not args.remove_NUMPC: args.remove_NUMPC=60
    if not args.remove_short: args.remove_short=5
    if not args.remove_URLPC: args.remove_URLPC=10
entrada=codecs.open(args.inputfile,"r",encoding="utf-8")
sortida=codecs.open(args.outputfile,"w",encoding="utf-8")


to_remove_long=False
if not args.remove_long==None:
    remove_longer_than=int(args.remove_long)
    to_remove_long=True

if args.stringFromFile:
    sfile=codecs.open(args.stringFromFile,"r",encoding="utf-8")
    remlist=[]
    for lsfile in sfile:
        lsfile=lsfile.rstrip()
        remlist.append(lsfile)
        
if args.regexFromFile:
    regfile=codecs.open(args.regexFromFile,"r",encoding="utf-8")
    reglist=[]
    for lsfile in regfile:
        lsfile=lsfile.rstrip()
        reglist.append(lsfile)

if args.vSL or args.vTL or args.vSetLanguages:
    import langid

if args.vSetLanguages:
    toset=[]
    for l in args.vSetLanguages.split(","):
        toset.append(l)
    langid.set_languages(toset)

for linia in entrada:
    toWrite=True
    linia=linia.strip()
    camps=linia.split("\t")
    if len(camps)>=1:
        slsegment=camps[0]
        tlsegment=""
    if len(camps)>=2:
        tlsegment=camps[1]
    if args.remove_control_characters:
        slsegment=remove_control_characters(slsegment)
        tlsegment=remove_control_characters(tlsegment) 
    if args.remove_non_printable:
        slsegment=remove_non_printable(slsegment)
        tlsegment=remove_non_printable(tlsegment)
    if args.unescape_html and toWrite:
        slsegment=unescape_html(slsegment)
        tlsegment=unescape_html(tlsegment)
    if args.fixencoding:
        slsegment=fix_encoding(slsegment)
        tlsegment=fix_encoding(tlsegment)
    if args.remove_tags and toWrite:
        slsegment=remove_tags(slsegment)
        tlsegment=remove_tags(tlsegment)
    if args.norm_unicode and toWrite:
        slsegment=unicodedata.normalize("NFKC", slsegment)
        tlsegment=unicodedata.normalize("NFKC", tlsegment)
    if args.check_weights and toWrite:
        if len(camps)<3 or not is_valid_float(camps[2]):
            toWrite=False
        
    if args.remove_non_latin:
        slsegment=remove_non_latin_extended_chars(slsegment)
        tlsegment=remove_non_latin_extended_chars(tlsegment)
    if args.remove_non_script:
        slsegment=remove_non_unicode_script_chars(slsegment)
        tlsegment=remove_non_unicode_script_chars(tlsegment)
    if to_remove_long and toWrite:
        if len(slsegment)>remove_longer_than:
            toWrite=False
        elif len(tlsegment)>remove_longer_than:
            toWrite=False
        
    if args.norm_apos and toWrite:
        slsegment=normalize_apos(slsegment)
        tlsegment=normalize_apos(tlsegment)
    if args.remove_empty and toWrite:
        if remove_empty(slsegment,tlsegment): toWrite=False
    if args.remove_short and toWrite:
        if remove_short(slsegment,args.remove_short): toWrite=False
    if args.remove_short and toWrite:
        if remove_short(slsegment,args.remove_short): toWrite=False
        if remove_short(tlsegment,args.remove_short): toWrite=False
    if args.remove_equal and toWrite:
        if remove_equal(slsegment,tlsegment): toWrite=False
    if args.remove_NUMPC and toWrite:
        if percentNUM(slsegment)>=float(args.remove_NUMPC):
            toWrite=False
        elif percentNUM(tlsegment)>=float(args.remove_NUMPC):
            toWrite=False
            
    if args.remove_URLPC and toWrite:
        if percentURLPC(slsegment)>=float(args.remove_NUMPC):
            toWrite=False
        elif percentURLPC(tlsegment)>=float(args.remove_NUMPC):
            toWrite=False
    if args.remove_URL and toWrite:
        urlsSL=findURLs(slsegment)
        urlsTL=findURLs(tlsegment)
        if len(urlsSL)>0 or len(urlsTL)>0:
            toWrite=False
        
        
            
    if args.escapeforMoses and toWrite:
        slsegment=escapeforMoses(slsegment)
        tlsegment=escapeforMoses(tlsegment)
    if args.vSL and toWrite:
        (lang,logpercent)=langid.classify(slsegment)
        if not args.vSL==lang:
                toWrite=False
                if args.verbose: print("SOURCE NOT MATCHING:",args.vSL,lang,slsegment)

    if args.vTL and toWrite:
        (lang,logpercent)=langid.classify(tlsegment)
        if not args.vTL==lang:
                toWrite=False
                if args.verbose: print("TARGET NOT MATCHING:",args.vTL,lang,tlsegment)
            
    if args.vTNOTL and toWrite:
        (lang,logpercent)=langid.classify(tlsegment)
        if args.vTNOTL==lang:
                toWrite=False
                if args.verbose: print("TARGET MATCHING:",args.vTNOTL,lang,tlsegment)
        

    if args.noUPPER and toWrite:
        if slsegment==slsegment.upper():
            toWrite=False
            if args.verbose: print("DELETE UPPER:",slsegment)
        if tlsegment==tlsegment.upper():
            toWrite=False
            if args.verbose: print("DELETE UPPER:",tlsegment)
                
    if args.stringFromFile and toWrite:
        for rmstring in remlist:
            if slsegment.find(rmstring)>-1:
                toWrite=False
                break
            if tlsegment.find(rmstring)>-1:
                toWrite=False
                break
                
    if args.regexFromFile and toWrite:
        for regex in reglist:
            pattern = re.compile(regex)
            if pattern.search(slsegment):
                toWrite=False
                break
            if pattern.search(tlsegment):
                toWrite=False
    if toWrite:
        if len(camps)==2:
            cadena=slsegment+"\t"+tlsegment
        elif len(camps)>2:
            cadena=slsegment+"\t"+tlsegment+"\t"+"\t".join(camps[2:])
        sortida.write(cadena+"\n")
        
