# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.utils import simplejson

import logging
logging.basicConfig()

import os
import sys
import subprocess

import HTMLParser
h = HTMLParser.HTMLParser()

import FALT as FALT

W = FALT.FALT()

def index(request):
	c = RequestContext(request, {'foo': 'bar',})
	return render_to_response('comp1/index.html', c)

def customRequest(request):
    global W
    words = request.GET['words']
    distance = int(request.GET['distance'])
    classes = request.GET['classes']
    try:
        ipa = request.GET['ipa']
    except:
        ipa = False;
    d = W.customRun(words, classes, distance, ipa)
    json = simplejson.dumps(d, sort_keys=True, indent=4)
    return HttpResponse(json, mimetype="application/json")

def mainRequest(request):
    return_dict = {}
    words = request.GET['words']
    size = int(request.GET['size'])

    global W 

    words = words.split(',')

    for word in words:
        word = word.encode('ascii', 'ignore')
        return_dict[word] = {}

        symbolized = W.symbolize(word, size)

        if symbolized[2] != '':
            if symbolized[1] != word.upper():
                similarities = W.getSimilarities(symbolized[1], size)
            else:
                similarities = W.getSimilarities(word, size)
            #data
            intSims = []
            extSims = []
            totalInts = 0
            totalExts = 0
            totalFreq = 0
            totalSims = 0
            tempFreq = 0
            avgFreq = 0
            if similarities != []:
                for similar in similarities[0]:
                    intSims.append(similar[0])
                    intSims.append(similar[1])
                    tempFreq += W.getFamiliarity(similar[0])
                totalInts += len(intSims)/2
                totalFreq += tempFreq
                if totalInts != 0:
                    return_dict[word]['internalFrequency'] = round(float(1.0*tempFreq/totalInts), 3)
                else:
                    return_dict[word]['internalFrequency'] = 0

                tempFreq = 0
                for similar in similarities[1]:
                    extSims.append(similar[0])
                    extSims.append(similar[1])
                    tempFreq += W.getFamiliarity(similar[0])
                totalExts += len(extSims)/2
                totalFreq += tempFreq
                if totalExts != 0:
                    return_dict[word]['externalFrequency'] = round(float(1.0*tempFreq/totalExts), 3)
                else:
                    return_dict[word]['externalFrequency'] = 0

                totalSims = totalInts + totalExts
                return_dict[word]['totalFrequency'] = round(float(1.0*totalFreq/totalSims), 3)
            return_dict[word]['internal'] = ' '.join(intSims)
            return_dict[word]['external'] = ' '.join(extSims)
            return_dict[word]['internalCount'] = totalInts
            return_dict[word]['externalCount'] = totalExts
            return_dict[word]['totalCount'] = totalSims
            return_dict[word]['symbolized'] = ''.join(symbolized[0])
            return_dict[word]['dictionary'] = symbolized[1]
            return_dict[word]['arpa'] = symbolized[2]
            return_dict[word]['ipa'] = symbolized[3]
            return_dict[word]['visemes'] = symbolized[4]
            return_dict[word]['syllables'] = countSyllables(word)
            return_dict[word]['wordFrequency'] = W.getFamiliarity(word)
        else:
            return_dict[word] = notFound(word.upper())
    json = simplejson.dumps(return_dict, sort_keys=False, indent=4)
    return HttpResponse(json, mimetype="application/json")

def notFound(word):
    return {
        "ipa": "", 
        "internalCount": 0, 
        "dictionary": word, 
        "externalCount": 0, 
        "totalFrequency": 0, 
        "arpa": "", 
        "internalFrequency": 0, 
        "totalCount": 0, 
        "internal": "", 
        "externalFrequency": 0, 
        "external": "", 
        "wordFrequency": 0, 
        "symbolized": "<small>Not found.</small>", 
        "syllables": 0, 
        "visemes": ""
    }

def fileRequest(request):
    return_dict = {}
    validExtensions = ['txt']
    error = 'None'
    for filename, file in request.FILES.iteritems():
        size = request.FILES[filename].size
        name = request.FILES[filename].name
        content = request.FILES[filename].read()

        if size > 2000000 or name.split(".")[-1] not in validExtensions:
            error = 'File must be < 2MB in size and in .txt format.' 
            return HttpResponse(error, mimetype="application/json")

    return_dict['filename'] = name
    return_dict['size'] = size
    return_dict['content'] = content
    json = simplejson.dumps(return_dict)
    return HttpResponse(json, mimetype="application/json")

import re
def countSyllables(word):
    word = word.lower()
    if len(word) < 3:
        count = 1
    elif word.endswith('e'):
        word = word[:-1]
    elif word.endswith('es'):
        word = word[:-2]
    elif word.endswith('ed'):
        word = word[:-2]
    count = len(re.findall('[aeiouy]+', word))
    if count == 0:
        count = 1
    return count
