# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.middleware.csrf import get_token
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

        #if symbolized[2] != '':
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
                tempFreq += int(W.getFamiliarity(similar[0]))
                totalInts += 1
            totalFreq += tempFreq
            try:
                return_dict[word]['internalFrequency'] = str(tempFreq/totalInts)
            except:
                return_dict[word]['internal'] = 0

            tempFreq = 0
            for similar in similarities[1]:
                extSims.append(similar[0])
                extSims.append(similar[1])
                tempFreq += int(W.getFamiliarity(similar[0]))
                totalExts += 1
            totalFreq += tempFreq
            try:
                return_dict[word]['externalFrequency'] = str(tempFreq/totalExts)
            except:
                return_dict[word]['externalFrequency'] = 0

            totalSims = totalInts + totalExts
            return_dict[word]['totalFrequency'] = str(totalFreq/totalSims)

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

    json = simplejson.dumps(return_dict, sort_keys=True, indent=4)
    return HttpResponse(json, mimetype="application/json")

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
