# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

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

def index(request):
	c = RequestContext(request, {'foo': 'bar',})
	return render_to_response('comp1/index.html', c)

def mainRequest(request):
    return_dict = {}
    words = request.GET['words']
    words = words.split(',')
    size = request.GET['size']

    for word in words:
        word = word.encode('ascii', 'ignore')
        return_dict[word] = {}
        return_dict[word]['syllables'] = countSyllables(word)
        return_dict[word]['symbolized'] = symbolizeWord(word, int(size))
        return_dict[word]['familiarity'] = getFamiliarity(word)
    json = simplejson.dumps(return_dict)
    return HttpResponse(json, mimetype="application/json")

def symbolizeWord(word, LECSize):
    W = FALT.FALT()
    return ''.join(W.symbolize(word, FALT.eqARPA[LECSize])[0])

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

def getFamiliarity(word):
    W = FALT.FALT()
    return W.getFamiliarity(word)
