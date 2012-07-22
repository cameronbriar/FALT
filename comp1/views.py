# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.middleware.csrf import get_token
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()

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
    words = words.split(',')
    size = request.GET['size']
    try:
        pretty = request.GET['pretty']
    except:
        pretty = False;

    for word in words:
        word = word.encode('ascii', 'ignore')

        symbolized = symbolizeWord(word, int(size))
        return_dict[word] = {}
        return_dict[word]['symbolized'] = ''.join(symbolized[0])
        return_dict[word]['dictionary'] = symbolized[1]
        return_dict[word]['arpa'] = symbolized[2]
        return_dict[word]['ipa'] = symbolized[3]
        return_dict[word]['visemes'] = ' '.join(str(x+1) for x in symbolized[4])
        return_dict[word]['syllables'] = countSyllables(word)
        return_dict[word]['familiarity'] = getFamiliarity(word)

    json = simplejson.dumps(return_dict)
    if pretty:
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

def symbolizeWord(word, LECSize):
    return W.symbolize(word, FALT.eqARPA[LECSize])

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

def getWordFromDictionary(word):
    return W.getWordFromDictionary(word)[0]

def getFamiliarity(word):
    return W.getFamiliarity(word)
