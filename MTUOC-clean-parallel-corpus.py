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
import langid
from bs4 import BeautifulSoup
import re
import regex as rx
from ftfy import fix_encoding
import unicodedata


def remove_non_latin_extended_chars(text):
    # Define the pattern to match only allowed characters
    # This includes basic Latin letters, Latin Extended characters, spaces, and common punctuation marks
    pattern = re.compile(r'[^A-Za-z\u00C0-\u00FF\u0100-\u024F\u1E00-\u1EFF\uA720-\uA7FF\s.,;!?\'"()\-]')
    
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
parser.add_argument('--remove_non_latin', action='store_true', dest='remove_non_latin', help='Removes chars outside the latin extended.')
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
        
