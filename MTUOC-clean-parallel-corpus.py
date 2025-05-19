#    MTUOC-clean-parallel-corpus
#    Copyright (C) 2025  Antoni Oliver
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

#    Segmentation is performed using srx_segmenter: https://github.com/narusemotoki/srx_segmenter
#    The code is copied into this script.

try:
    import tkinter 
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfilename
except:
    pass
import itertools
import codecs
import sys

import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
###
import re
from xml.sax.saxutils import unescape
import html
import argparse
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

###


def select_input_file():
    global E1
    infile = askopenfilename(initialdir = ".",filetypes =(("txt files","*.txt"),("All Files","*.*")),
                           title = "Select the input file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)
    
def select_output_file():
    global E2
    infile = asksaveasfilename(initialdir = ".",filetypes =(("txt files","*.txt"),("All Files","*.*")),
                           title = "Select the output file.")
    E2.delete(0,END)
    E2.insert(0,infile)
    E2.xview_moveto(1)

def select_config_file():
    global E3
    infile = askopenfilename(initialdir = ".",filetypes =(("yaml files","*.yaml"),("All Files","*.*")),
                           title = "Select the config file.")
    E3.delete(0,END)
    E3.insert(0,infile)
    E3.xview_moveto(1)

def go(configfile=None,inputfile=None,outputfile=None):
    if configfile==None:
        global E3
        configfile=E3.get()
    if inputfile==None:
        global E1
        inputfile=E1.get()
    if outputfile==None:
        global E2
        outputfile=E2.get()
    stream = open(configfile, 'r',encoding="utf-8")
    configYAML=yaml.load(stream, Loader=yaml.FullLoader)

    remove_control_charactersA=configYAML["remove_control_characters"]
    remove_non_printableA=configYAML["remove_non_printable"]
    norm_aposA=configYAML["norm_apos"]
    norm_unicodeA=configYAML["norm_unicode"]
    remove_tagsA=configYAML["remove_tags"]
    unescape_htmlA=configYAML["unescape_html"]
    fixencodingA=configYAML["fixencoding"]
    remove_emptyA=configYAML["remove_empty"]
    remove_shortA=configYAML["remove_short"]
    remove_equalA=configYAML["remove_equal"]
    remove_NUMPCA=configYAML["remove_NUMPC"]
    remove_URLPCA=configYAML["remove_URLPC"]
    remove_URLA=configYAML["remove_URL"]
    remove_longA=configYAML["remove_long"]
    remove_non_latinA=configYAML["remove_non_latin"]
    remove_non_scriptA=configYAML["remove_non_script"]
    check_weightsA=configYAML["check_weights"]
    escapeforMosesA=configYAML["escapeforMoses"]
    stringFromFileA=configYAML["stringFromFile"]
    regexFromFileA=configYAML["regexFromFile"]
    vSLA=configYAML["vSL"]
    vTLA=configYAML["vTL"]
    vSetLanguagesA=configYAML["vSetLanguages"]
    vTNOTLA=configYAML["vTNOTL"]
    noUPPERA=configYAML["noUPPER"]
    verbose=configYAML["verbose"]
    
    ####
    entrada=codecs.open(inputfile,"r",encoding="utf-8")
    sortida=codecs.open(outputfile,"w",encoding="utf-8")


    to_remove_long=False
    if not remove_longA==False:
        remove_longer_than=int(remove_long)
        to_remove_long=True

    if stringFromFileA:
        sfile=codecs.open(stringFromFile,"r",encoding="utf-8")
        remlist=[]
        for lsfile in sfile:
            lsfile=lsfile.rstrip()
            remlist.append(lsfile)
            
    if regexFromFileA:
        regfile=codecs.open(regexFromFile,"r",encoding="utf-8")
        reglist=[]
        for lsfile in regfile:
            lsfile=lsfile.rstrip()
            reglist.append(lsfile)

    if vSLA or vTLA or vSetLanguagesA:
        import langid

    if vSetLanguagesA:
        toset=[]
        for l in vSetLanguagesA.split(","):
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
        if remove_control_charactersA:
            slsegment=remove_control_characters(slsegment)
            tlsegment=remove_control_characters(tlsegment) 
        if remove_non_printableA:
            slsegment=remove_non_printable(slsegment)
            tlsegment=remove_non_printable(tlsegment)
        if unescape_htmlA and toWrite:
            slsegment=unescape_html(slsegment)
            tlsegment=unescape_html(tlsegment)
        if fixencodingA and  toWrite:
            slsegment=fix_encoding(slsegment)
            tlsegment=fix_encoding(tlsegment)
        if remove_tagsA and toWrite:
            slsegment=remove_tags(slsegment)
            tlsegment=remove_tags(tlsegment)
        if norm_unicodeA and toWrite:
            slsegment=unicodedata.normalize("NFC", slsegment)
            tlsegment=unicodedata.normalize("NFC", tlsegment)
        if check_weightsA and toWrite:
            if len(camps)<3 or not is_valid_float(camps[2]):
                toWrite=False
            
        if remove_non_latinA:
            slsegment=remove_non_latin_extended_chars(slsegment)
            tlsegment=remove_non_latin_extended_chars(tlsegment)
        if remove_non_scriptA:
            slsegment=remove_non_unicode_script_chars(slsegment)
            tlsegment=remove_non_unicode_script_chars(tlsegment)
        if to_remove_long and toWrite:
            if len(slsegment)>remove_longer_than:
                toWrite=False
            elif len(tlsegment)>remove_longer_than:
                toWrite=False
            
        if norm_aposA and toWrite:
            slsegment=normalize_apos(slsegment)
            tlsegment=normalize_apos(tlsegment)
        if remove_emptyA and toWrite:
            if remove_empty(slsegment,tlsegment): toWrite=False
        if remove_shortA > -1 and toWrite:
            if remove_short(slsegment,remove_shortA): toWrite=False
            if remove_short(tlsegment,remove_shortA): toWrite=False
        if remove_equalA and toWrite:
            if remove_equal(slsegment,tlsegment): toWrite=False
        if remove_NUMPCA and toWrite:
            if percentNUM(slsegment)>=float(remove_NUMPCA):
                toWrite=False
            elif percentNUM(tlsegment)>=float(remove_NUMPCA):
                toWrite=False
                
        if remove_URLPCA and toWrite:
            if percentURLPC(slsegment)>=float(remove_NUMPCA):
                toWrite=False
            elif percentURLPC(tlsegment)>=float(remove_NUMPCA):
                toWrite=False
        if remove_URLA and toWrite:
            urlsSL=findURLs(slsegment)
            urlsTL=findURLs(tlsegment)
            if len(urlsSL)>0 or len(urlsTL)>0:
                toWrite=False
            
            
                
        if escapeforMosesA and toWrite:
            slsegment=escapeforMoses(slsegment)
            tlsegment=escapeforMoses(tlsegment)
        if vSLA and toWrite:
            (lang,logpercent)=langid.classify(slsegment)
            if not vSLA==lang:
                    toWrite=False
                    if verbose: print("SOURCE NOT MATCHING:",vSLA,lang,slsegment)

        if vTLA and toWrite:
            (lang,logpercent)=langid.classify(tlsegment)
            if not vTLA==lang:
                    toWrite=False
                    if verbose: print("TARGET NOT MATCHING:",vTLA,lang,tlsegment)
                
        if vTNOTLA and toWrite:
            (lang,logpercent)=langid.classify(tlsegment)
            if vTNOTLA==lang:
                    toWrite=False
                    if verbose: print("TARGET MATCHING:",vTNOTL,lang,tlsegment)
            

        if noUPPERA and toWrite:
            if slsegment==slsegment.upper():
                toWrite=False
                if verbose: print("DELETE UPPER:",slsegment)
            if tlsegment==tlsegment.upper():
                toWrite=False
                if verbose: print("DELETE UPPER:",tlsegment)
                    
        if stringFromFileA and toWrite:
            for rmstring in remlist:
                if slsegment.find(rmstring)>-1:
                    toWrite=False
                    break
                if tlsegment.find(rmstring)>-1:
                    toWrite=False
                    break
                    
        if regexFromFileA and toWrite:
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
        

    

def launch_gui():
    top = Tk()
    top.title("MTUOC-clean-parallel-corpus")
    global E1
    global E2
    global E3
    
    B1=tkinter.Button(top, text = str("Select input file"), borderwidth = 1, command=select_input_file,width=14).grid(row=0,column=0)
    E1 = tkinter.Entry(top, bd = 5, width=60, justify="right")
    E1.grid(row=0,column=1)

    B2=tkinter.Button(top, text = str("Select output file"), borderwidth = 1, command=select_output_file,width=14).grid(row=1,column=0)
    E2 = tkinter.Entry(top, bd = 5, width=60, justify="right")
    E2.grid(row=1,column=1)
    
    B3=tkinter.Button(top, text = str("Select config file"), borderwidth = 1, command=select_config_file,width=14).grid(row=2,column=0)
    E3 = tkinter.Entry(top, bd = 5, width=60, justify="right")
    E3.grid(row=2,column=1)

    B2=tkinter.Button(top, text = str("Clean!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=3,column=0)

    top.mainloop()
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No parameters, start the GUI
        launch_gui()
    else:
        # Parameters provided, perform the action
        if len(sys.argv)<4:
            print("ERROR: wrong number of parameters given.")
            print("USAGE:")
            print("    Give no parameters to start the GUI or:")
            print("    python MTUOC-clean-parallel-corpus.py config.yaml inputcorpus cleanedcorpus")
        else:
            go(sys.argv[1],sys.argv[2],sys.argv[3])






