#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from wagnerfischer import WagnerFischer
import base64
import html5lib
from lxml import etree
import re
import argparse
import hashlib

parser = argparse.ArgumentParser(description='Given Bitextor DOCALG segments (stdin) and the deferred Bitextor crawl from deferred document script (positional argument), returns segments stand-off annotations in DOCALG format (stdout)')
parser.add_argument('deferred_crawl_path', help='path of deferred crawl file')

args = parser.parse_args()

#Argument input: deferred Bitextor crawl file with plain text and its standoff annotations (output of deferred document script)
documentStandoff = dict()
with open(args.deferred_crawl_path,'r') as reader:
    for line in reader:
        fields = line.split('\t')
        fields = list(map(str.strip, fields))
        documenttext = base64.b64decode(fields[0]).decode('utf8')
        documentStandoff[fields[1]]=(documenttext,fields[3].split(';'))

#Input (stdin): Bitextor DOCALG file:
#url1 url2 clean_text1_in_base64 clean_text2_in_base64 [...]

#Output (stdout): Bitextor DOCALG file:
#url1 url2 clean_text1_in_base64 clean_text2_in_base64 [...] standoff_text1 standoff_text2
sl_document_sentences_list=[]
tl_document_sentences_list=[]
sl_document_url=""
tl_document_url=""

def print_standoff_from_buffer(sl_document_sentences_list,tl_document_sentences_list,sl_document_url,tl_document_url,documentStandoff):
    shortpathSL=WagnerFischer([x for x in " ".join(sl_document_sentences_list).replace('\n',' ').replace('\t',' ').replace('\xa0',' ').split(' ') if x != ''],[x for x in documentStandoff[sl_document_url][0].replace('\n',' ').replace('\t',' ').replace('\xa0',' ').split(' ') if x != '']).optimum_alignments() #Calculate a short distance path using Wagner-Fischer algorithm for source
    shortpathTL=WagnerFischer([x for x in " ".join(tl_document_sentences_list).replace('\n',' ').replace('\t',' ').replace('\xa0',' ').split(' ') if x != ''],[x for x in documentStandoff[tl_document_url][0].replace('\n',' ').replace('\t',' ').replace('\xa0',' ').split(' ') if x != '']).optimum_alignments() #and target sentences

    standoffSL=[]
    standoffTL=[]
    position=0

    for op in shortpathSL: #Obtain the standoff annotation of each sentence word from the full annotated document they come from, counting non-inserted words
        if op != "I":
            standoffSL.append(documentStandoff[sl_document_url][1][position])
        position = position + 1

    position=0
    for op in shortpathTL: #Same for TL
        if op != "I":
            standoffTL.append(documentStandoff[tl_document_url][1][position])
        position = position + 1

    positionSL=0
    positionTL=0
    for sl_sentence,tl_sentence in zip(sl_document_sentences_list,tl_document_sentences_list):
        buffered_line_fields=[sl_document_url, tl_document_url, sl_sentence, tl_sentence]
        if sl_sentence == "":
            buffered_line_fields.append("")
            buffered_line_fields.append(hashlib.md5(b"").hexdigest()) #MD5 document checksum
        else:
            buffered_line_fields.append(";".join(standoffSL[positionSL:positionSL+len(sl_sentence.split(' '))]))
            buffered_line_fields.append(hashlib.md5(sl_sentence.encode('utf8')).hexdigest()) #MD5 document checksum
            positionSL = positionSL+len(sl_sentence.split(' '))

        if tl_sentence == "":
            buffered_line_fields.append("")
            buffered_line_fields.append(hashlib.md5(b"").hexdigest()) #MD5 document checksum
        else:
            buffered_line_fields.append(";".join(standoffTL[positionTL:positionTL+len(tl_sentence.split(' '))]))
            buffered_line_fields.append(hashlib.md5(tl_sentence.encode('utf8')).hexdigest()) #MD5 document checksum
            positionTL = positionTL+len(tl_sentence.split(' '))

        #TODO: simplify the sentence standoff annotation joining/collapsing word standoff annotations with the same tag path

        print("\t".join(buffered_line_fields))

for line in sys.stdin:
    fields = line.split('\t')
    fields = list(map(str.strip, fields)) #Strip all elements
    
    if sl_document_url != "" and fields[0] != sl_document_url:
        print_standoff_from_buffer(sl_document_sentences_list,tl_document_sentences_list,sl_document_url,tl_document_url,documentStandoff)
        sl_document_sentences_list = []
        tl_document_sentences_list = []

    sl_document_url = fields[0]
    sl_document_sentences_list.append(fields[2].strip())
    tl_document_url = fields[1]
    tl_document_sentences_list.append(fields[3].strip())

print_standoff_from_buffer(sl_document_sentences_list,tl_document_sentences_list,sl_document_url,tl_document_url,documentStandoff)
