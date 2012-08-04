#!/usr/bin/python
#!encoding=utf-8

# The FRESNO AUDIOVISUAL LEXICON TOOL is an open source project under the MIT license.

# The MIT License (MIT)
# Copyright (c) 2012 Fresno State

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import io
import re
import sys
import time
import marshal
import subprocess
import Levenshtein as L
import time

# FALT : Fresno Audiovisual Lexicon Tool
# version 0.10

# this is the name of the Carnegie Melon University ARPA dictionary
# it has been modified with the IPA equivalence
# default location: /static/
defaultFilename = "cmudict_ARPA_IPA_m"
dictionaryWords = "words_all_m"
dictionaryFreqs = "words_freq_m"
# the symbols used for representing viseme sets
# must remain in same order as symbols.keys()
symbols = {'crosshatch': [u'\u25a9', '&#9641;'], 'snowman': [u'\u2603', '&#9731;'], 'at': [u'@', '&#64;'], 'female': [u'\u2640', '&#9792;'], 'scissors': [u'\u2704', '&#9988;'], 'airplane': [u'\u2708', '&#9992;'], 'cloud': [u'\u2601', '&#9729;'], 'fourpoint': [u'\u2726', '&#10022;'], 'flower': [u'\u273f', '&#10047;'], 'phonemic': [u'\u260e', '&#9742;'], 'sun': [u'\u2742', '&#10050;'], 'peace': [u'\u270c', '&#9996;'], 'blackstar': [u'\u2738', '&#10040;'], 'elevator': [u'\u27e0', '&#10208;'], 'chess': [u'\u265a', '&#9818;'], 'smile': [u'\u263a', '&#9786;'], 'circle': [u'\u29bf', '&#10687;'], 'wheel': [u'\u2638', '&#9784;'], 'pencil': [u'\u270f', '&#9998;'], 'coffee': [u'\u2668', '&#9832;'], 'umbrella': [u'\u2602', '&#9730;'], 'perceive': [u'\u25f5', '&#9717;'], 'mac': [u'\u2318', '&#8984;'], 'eject': [u'\u23cf', '&#9167;'], 'medical': [u'\u2624', '&#9764;'], 'biohazard': [u'\u2623', '&#9763;'], 'blackdiamond': [u'\u2756', '&#10070;'], 'castle': [u'\u2656', '&#9814;'], 'star': [u'\u2605', '&#9733;'], 'sagit': [u'\u2650', '&#9808;']}

# dictionary to convert ARPA -> IPA
arpaToIPA = {'IH': u'\u026a', 'UH R': u'\u028ar', 'ER' : u'\u025d', 'UH' : u'\u028a', 'UW' : 'u', 'IH': u'\u026a', 'AH': u'\u028c', 'AA R': u'\u0251r', 'AH': u'\u0259', 'AH': u'\u028c', 'JH': u'd\u0292', 'AW R': u'a\u028ar', 'EH': u'\u025b', 'EH': u'\u025b', 'EH': u'\u025b', 'EY': u'e\u026a', 'AO R': u'\u0254r', 'EY': u'e\u026a', 'EH R': u'\u025br', 'AY': u'a\u026a', 'IH': u'\u026a', 'AY': u'a\u026a', 'R': u'\u0279', 'D': u'd', 'AO R': u'\u0254r', 'AW': u'a\u028a', 'AW': u'a\u028a', 'AW': u'a\u028a', 'P': u'p', 'AO': u'\u0254', 'AX': u'\u028c', 'IH R': u'\u026ar', 'IY R': u'\u026ar', 'OY': u'\u0254\u026a', 'UH R': u'\u028ar', 'UW': u'u', 'HH': u'h', 'UH': u'\u028a', 'EH R': u'\u025br', 'AO R': u'\u0254r', 'ZH': u'\u0292', 'G': u'\u0261', 'K': u'k', 'S': u's', 'IH R': u'\u026ar', 'W': u'w', 'AE': u'\xe6', 'AE': u'\xe6', 'IH R': u'\u026ar', 'AW R': u'a\u028ar', 'EY': u'e\u026a', 'NG': u'\u014b', 'CH': u't\u0283', 'F': u'f', 'N': u'n', 'R': u'\u0279', 'V': u'v', 'Z': u'z', 'MEYE': u'm\xe6', 'AY': u'a\u026a', 'SH': u'\u0283', 'AW R': u'a\u028ar', 'DH': u'\xf0', 'IY R': u'\u026ar', 'B': u'b', 'DX': u'\u027e', 'AA R': u'\u0251r', 'TH': u'\u03b8', 'IY': u'i', 'M': u'm', 'L': u'l', 'IH': u'\u026a', 'IY R': u'\u026ar', 'Y': u'j', 'OW': u'o\u028a', 'ER': u'\u025d', 'IY': u'i', 'AA': u'\u0251', 'T': u't'}

# dictionary to convert IPA -> ARPA
ipaToARPA = {u'\u0283': 'SH', u'\u025d' : 'ER', u't\u0361\u0283' : 'CH', u'd\u0361\u0292' : 'JH', 'u' : 'UW', u'a\u028a': 'AW', u'o\u028a': 'OW', u'e\u026a': 'EY', u'a\u028ar': 'AW R', u'a\u026a': 'AY', u'\u0254r': 'AO R', u'\u028c': 'AH', u'\u0292': 'ZH', u'\u0254\u026a': 'OY2', u'\u025br': 'EH R', u'\xf0': 'DH', u'j': 'Y', u'\u03b8': 'TH', u'b': 'B', u'd\u0292': 'JH', u'\u0251r': 'AA R',  u'\u014b': 'NG', u'\u026ar': 'IH R', u'\u026ar': 'IH R', u'\u0251': 'AA', u'm\xe6': 'MEYE', u'\u0254': 'AO', u'\u0259': 'AH', u'\u025b': 'EH', u'\u025a': 'ER', u'\u025d': 'ER', u't\u0283': 'CH', u'\u0261': 'G', u'f': 'F', u'd': 'D', u'\xe6': 'AE', u'i': 'IY', u'h': 'HH', u'k': 'K', u'\u026a': 'IH', u'm': 'M', u'l': 'L', u'\u028ar': 'UH R', u'n': 'N', u'r': 'R', u'\u028a': 'UH', u'p': 'P', u's': 'S', u'u': 'UW', u't': 'T', u'w': 'W', u'v': 'V', u'\u0279': 'R', u'z': 'Z', u'\u027e': 'DX'}

# visemic classes as seen in auer and bernstein
# http://cloudedbox.com/FALT/auerandbernstein.pdf
#eqIPA = {}
#eqIPA[28] = [ ['ʊ'], ['u'], ['eɪ'], ['oʊ'], ['aʊ'], ['ɪ', 'i'], ['ɛ'], ['æ'], ['ɔɪ'], ['ɔ'], ['aɪ'], ['ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l'], ['n'], ['k'], ['ɡ', 'ŋ'], ['h'], ['d'], ['t'], ['s', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ'], ['tʃ'], ['ʒ'], ['dʒ']]
#eqIPA[19] = [ ['ʊ', 'u', 'eɪ'], ['oʊ', 'aʊ'], ['ɪ', 'i'], ['ɛ'], ['æ'], ['ɔɪ'], ['ɔ'], ['aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l'], ['n', 'k'], ['ɡ', 'ŋ'], ['h'], ['d'], ['t', 's', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ', 'tʃ', 'ʒ', 'dʒ']]
#eqIPA[12] = [ ['ʊ', 'u', 'eɪ'], ['oʊ', 'aʊ'], ['ɪ', 'i', 'ɛ','æ'], ['ɔɪ'], ['ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l','n', 'k','ɡ', 'ŋ','h'], ['d','t', 's', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ', 'tʃ', 'ʒ', 'dʒ']]
#eqIPA[10] = [ ['ʊ', 'u', 'eɪ'], ['oʊ', 'aʊ'], ['ɪ', 'i', 'ɛ','æ'], ['ɔɪ' ,'ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l', 'n', 'k', 'ɡ', 'ŋ', 'h', 'd', 't', 's', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ', 'tʃ', 'ʒ', 'dʒ']]
#eqIPA[2] =  [ ['ʊ', 'u', 'eɪ', 'oʊ', 'aʊ', 'ɪ', 'i', 'ɛ','æ', 'ɔɪ' ,'ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm', 'v', 'f', 'l', 'n', 'k', 'ɡ', 'ŋ', 'h', 'd', 't', 's', 'z', 'r', 'w', 'ð', 'θ', 'ʃ', 'tʃ', 'ʒ', 'dʒ']]
#eqIPA[1] =  [ ['ʊ', 'u', 'eɪ', 'oʊ', 'aʊ', 'ɪ', 'i', 'ɛ','æ', 'ɔɪ' ,'ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j', 'p', 'b', 'm', 'v', 'f', 'l', 'n', 'k', 'ɡ', 'ŋ', 'h', 'd', 't', 's', 'z', 'r', 'w', 'ð', 'θ', 'ʃ', 'tʃ', 'ʒ', 'dʒ']]

eqARPA = {1: [[['UH2', 'UH0', 'UH1'], ['UW2', 'UW1', 'UW0'], ['ER1', 'ER0', 'ER2'], ['EY1', 'EY0', 'EY2'], ['OW1', 'OW0', 'OW2'], ['AW1', 'AW0', 'AW2'], ['IH2', 'IH2', 'IH1', 'IH0', 'IH'], ['IY1', 'IY0', 'IY2'], ['EH2', 'EH0', 'EH1'], ['AE1', 'AE0', 'AE2'], ['OY2', 'OY1', 'OY0'], ['AO2', 'AO1', 'AO0'], ['AY1', 'AY0', 'AY2'], ['AH2', 'AH1', 'AX0'], ['AH0'], ['AA0', 'AA2', 'AA1'], ['Y'], ['P'], ['B'], ['M'], ['V'], ['F'], ['L'], ['N'], ['K'], ['G'], ['NG'], ['HH'], ['D'], ['T'], ['S'], ['Z'], ['R'], ['W'], ['DH'], ['TH'], ['SH'], ['CH'], ['ZH'], ['JH']]], 2: [[['UH2', 'UH0', 'UH1'], ['UW2', 'UW1', 'UW0'], ['ER1', 'ER0', 'ER2'], ['EY1', 'EY0', 'EY2'], ['OW1', 'OW0', 'OW2'], ['AW1', 'AW0', 'AW2'], ['IH2', 'IH2', 'IH1', 'IH0', 'IH'], ['IY1', 'IY0', 'IY2'], ['EH2', 'EH0', 'EH1'], ['AE1', 'AE0', 'AE2'], ['OY2', 'OY1', 'OY0'], ['AO2', 'AO1', 'AO0'], ['AY1', 'AY0', 'AY2'], ['AH2', 'AH1', 'AX0'], ['AH0'], ['AA0', 'AA2', 'AA1'], ['Y']], [['P'], ['B'], ['M'], ['V'], ['F'], ['L'], ['N'], ['K'], ['G'], ['NG'], ['HH'], ['D'], ['T'], ['S'], ['Z'], ['R', 'R0'], ['W'], ['DH'], ['TH'], ['SH'], ['CH'], ['ZH'], ['JH']]], 10: [[['UH2', 'UH0', 'UH1'], ['UW2', 'UW1', 'UW0'], ['ER1', 'ER0', 'ER2'], ['EY1', 'EY0', 'EY2']], [['OW1', 'OW0', 'OW2'], ['AW1', 'AW0', 'AW2']], [['IH2', 'IH2', 'IH1', 'IH0', 'IH'], ['IY1', 'IY0', 'IY2'], ['EH2', 'EH0', 'EH1'], ['AE1', 'AE0', 'AE2']], [['OY2', 'OY1', 'OY0'], ['AO2', 'AO1', 'AO0'], ['AY1', 'AY0', 'AY2'], ['AH2', 'AH1', 'AX0'], ['AH0'], ['AA0', 'AA2', 'AA1'], ['Y']], [['P'], ['B'], ['M']], [['V'], ['F']], [['L'], ['N'], ['K'], ['G'], ['NG'], ['HH'], ['D'], ['T'], ['S'], ['Z']], [['R'], ['W']], [['DH'], ['TH']], [['SH'], ['CH'], ['ZH'], ['JH']]], 12: [[['UH2', 'UH0', 'UH1'], ['UW2', 'UW1', 'UW0'], ['EY1', 'EY0', 'EY2'], ['ER1', 'ER0', 'ER2']], [['OW1', 'OW0', 'OW2'], ['AW1', 'AW0', 'AW2']], [['IH2', 'IH2', 'IH1', 'IH0', 'IH'], ['IY1', 'IY0', 'IY2'], ['EH2', 'EH0', 'EH1'], ['AE1', 'AE0', 'AE2']], [['OY2', 'OY1', 'OY0']], [['AO2', 'AO1', 'AO0'], ['AY1', 'AY0', 'AY2'], ['AH2', 'AH1', 'AX0'], ['AH0'], ['AA0', 'AA2', 'AA1'], ['Y']], [['P'], ['B'], ['M']], [['V'], ['F']], [['L'], ['N'], ['K'], ['G'], ['NG'], ['HH']], [['D'], ['T'], ['S'], ['Z']], [['R'], ['W']], [['DH'], ['TH']], [['SH'], ['CH'], ['ZH'], ['JH']]], 19: [[['UH2', 'UH0', 'UH1'], ['UW2', 'UW1', 'UW0'], ['ER1', 'ER0', 'ER2'], ['EY1', 'EY0', 'EY2']], [['OW1', 'OW0', 'OW2'], ['AW1', 'AW0', 'AW2']], [['IH2', 'IH2', 'IH1', 'IH0', 'IH'], ['IY1', 'IY0', 'IY2']], [['EH2', 'EH0', 'EH1']], [['AE1', 'AE0', 'AE2']], [['OY2', 'OY1', 'OY0']], [['AO2', 'AO1', 'AO0']], [['AY1', 'AY0', 'AY2'], ['AH2', 'AH1', 'AX0'], ['AH0'], ['AA0', 'AA2', 'AA1'], ['Y']], [['P'], ['B'], ['M']], [['V'], ['F']], [['L']], [['N'], ['K']], [['G'], ['NG']], [['HH']], [['D']], [['T'], ['S'], ['Z']], [['R'], ['W']], [['DH'], ['TH']], [['SH'], ['CH'], ['ZH'], ['JH']]], 28: [[['UH2', 'UH0', 'UH1']], [['UW2', 'UW1', 'UW0']], [['EY1', 'EY0', 'EY2', 'ER1', 'ER0', 'ER2']], [['OW1', 'OW0', 'OW2']], [['AW1', 'AW0', 'AW2']], [['IH2', 'IH2', 'IH1', 'IH0', 'IH'], ['IY1', 'IY0', 'IY2']], [['EH2', 'EH0', 'EH1']], [['AE1', 'AE0', 'AE2']], [['OY2', 'OY1', 'OY0']], [['AO2', 'AO1', 'AO0']], [['AY1', 'AY0', 'AY2']], [['AH2', 'AH1', 'AX0'], ['AH0'], ['AA0', 'AA2', 'AA1'], ['Y']], [['P'], ['B'], ['M']], [['V'], ['F']], [['L']], [['N']], [['K']], [['G'], ['NG']], [['HH']], [['D']], [['T']], [['S'], ['Z']], [['R'], ['W']], [['DH'], ['TH']], [['SH']], [['CH']], [['ZH']], [['JH']]]}
#eqARPA = {1: [['UH', 'UW', 'EY', 'OW', 'AW', 'IH', 'IY', 'EH', 'AE', 'OY', 'AO', 'AY', 'AH', 'AH0', 'AA', 'Y', 'P', 'B', 'M', 'V', 'F', 'L', 'N', 'K', 'G', 'NG', 'HH', 'D', 'T', 'S', 'Z', 'R', 'W', 'DH', 'TH', 'SH', 'CH', 'ZH', 'JH']], 2: [['UH', 'UW', 'EY', 'OW', 'AW', 'IH', 'IY', 'EH', 'AE', 'OY', 'AO', 'AY', 'AH', 'AH0', 'AA', 'Y'], ['P', 'B', 'M', 'V', 'F', 'L', 'N', 'K', 'G', 'NG', 'HH', 'D', 'T', 'S', 'Z', 'R', 'W', 'DH', 'TH', 'SH', 'CH', 'ZH', 'JH']], 10: [['UH', 'UW', 'EY'], ['OW', 'AW'], ['IH', 'IY', 'EH', 'AE'], ['OY', 'AO', 'AY', 'AH', 'AH0', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L', 'N', 'K', 'G', 'NG', 'HH', 'D', 'T', 'S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH', 'CH', 'ZH', 'JH']], 12: [['UH', 'UW', 'EY'], ['OW', 'AW'], ['IH', 'IY', 'EH', 'AE'], ['OY'], ['AO', 'AY', 'AH', 'AH0', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L', 'N', 'K', 'G', 'NG', 'HH'], ['D', 'T', 'S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH', 'CH', 'ZH', 'JH']], 19: [['UH', 'UW', 'EY'], ['OW', 'AW'], ['IH', 'IY'], ['EH'], ['AE'], ['OY'], ['AO'], ['AY', 'AH', 'AH0', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L'], ['N', 'K'], ['G', 'NG'], ['HH'], ['D'], ['T', 'S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH', 'CH', 'ZH', 'JH']], 28: [['UH'], ['UW'], ['EY'], ['OW'], ['AW'], ['IH', 'IY'], ['EH'], ['AE'], ['OY'], ['AO'], ['AY'], ['AH', 'AH0', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L'], ['N'], ['K'], ['G', 'NG'], ['HH'], ['D'], ['T'], ['S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH'], ['CH'], ['ZH'], ['JH']]}


class FALT(object):
	def __init__(self):
		print 'Initializing FALT...'
		start = time.time()
		#self.equivalence = self.initEquivalence(size)
		self.dictWords = open(dictionaryWords, "rb")
		self.dictionary = marshal.load(self.dictWords)
		self.dictWords.close()
		self.index = { 1 : 0, 2 : 1, 10 : 2, 12 : 3, 19 : 4, 28 : 5 }
		self.dictWords = open(defaultFilename)
		self.phonemes = marshal.load(self.dictWords)
		self.dictWords.close()
		self.dictWords = open('words_freq_m')
		self.familiarity = marshal.load(self.dictWords)
		self.dictWords.close()
		self.result = []
		elapsed = (time.time() - start)
		print 'FALT is READY in', str(elapsed), 's'
		return

	def getDictionary(self, filename=defaultFilename, delimiter="  "):
		# stores dictionary file in dictionary
		# precondition: file is delimited with "  " and has 3 columns
		import codecs
		d = {}
		dictionary = codecs.open(filename, 'r', 'utf-8')
		for line in dictionary:
			info = line.split(delimiter)
			d[info[0]] = [info[1], info[2]]
		return d

	def getDictionaryCount(self, filename=defaultFilename):
		# uses wc to compute number of lines in file
		p = subprocess.Popen("wc -l '"+filename+"' | awk '{print $1}'", shell=True, stdout=subprocess.PIPE)
		result = p.communicate()[0]
		result = int(result.replace("\n", ""))
		return result

	def getWordFromDictionary(self, word, filename=defaultFilename):
		word = word.upper()
		self.result = []
		print word
		if self.phonemes.has_key(word):
			self.result.append(word)
			self.result.append(self.phonemes[word][0])
			self.result.append(self.phonemes[word][1])
	   	# if there is no exact match, try a rough match
	   	#else:
	   		#p = subprocess.Popen("grep -i --line-buffered '"+word+"' "+filename, shell=True, stdout=subprocess.PIPE)
	   		#self.result = p.communicate(None)[0].split("\n")[0].split("  ")

	   	if self.result == []:
	   		return [word, '', '']
	   	# resul = [ word , ARPA, IPA ]
   		return self.result

   	def initEquivalence(self, size):
   		#returns a dictionary with ARPA keys
   		#and viseme class values
   		d = {}
   		for i, sets in enumerate(eqARPA[size]):
   			for group in sets:
   				for phoneme in group:
   					d[phoneme] = i
   		return d

   	def ipaToArpa(self, phoneme):
   		return ipaToARPA[phoneme.decode('utf-8')]

   	def symbolize(self, word, size):
   		info = self.getWordFromDictionary(word)
   		# if there was not entry for the word
   		if info[1] == '':
   			return ['<small>Not found.</small>', '', '', '', '']
   		index = self.index[size]
   		symbolized = self.dictionary[info[0]][-1][index]
   		visemeSet = self.dictionary[info[0]][index]
   		# [symbolized version, original word, arpa, ipa, viseme classes]
   		return [symbolized, info[0], info[1], info[2], visemeSet]

   	def getSimilarities(self, word, size, maxDistance=1):
   		if word == '':
   			return []
   		similar = []
   		internal = []
   		external = []
   		total = 0
   		index = self.index[size]
   		word = word.upper()
   		for eachWord in self.dictionary:
   			if abs(len(self.dictionary[word][-1][index]) - len(self.dictionary[eachWord][-1][index])) > 0:
   				continue
   			else:
   				try:
   					distance = L.distance(''.join(self.dictionary[eachWord][-1][index]), ''.join(self.dictionary[word][-1][index]))
					if distance == 0:
						internal.append((eachWord, ''.join(self.dictionary[eachWord][-1][index])))
						total += 1
					elif distance <= maxDistance:
						external.append((eachWord, ''.join(self.dictionary[eachWord][-1][index])))
						total += 1
				except:
					continue
   		return (internal, external)

	def getFamiliarity(self, word):
		# numbers from WordNet
		word = word.upper()
		try:
			return self.familiarity[word]
		except:
			return 0
	# Custom Fun
	def customRun(self, words = "", classes = "", distance = 1, ipa = False):
		#parse words
		words = words.split(",")
		#parse classes
		classes = classes.split("|")
		newClasses = {}
		phonToSym = {}
		#parse groups & symbols
		for i, visemeClass in enumerate(classes):
			num = i+1
			group = visemeClass.split(",")
			newClasses[num] = []
			for phoneme in group:
				if ipa:
					try:
						translated = ipaToARPA(phoneme)
						newClasses[num].append(translated)
						newClasses[phoneme] = str(num)
						phonToSym[translated] = symbols[symbols.keys()[num]][0]
					except:
						print 'appending ?'
						newClasses[num].append('?')
						newClasses[phoneme] = '?'
				else:
					phoneme = re.sub(r'[0-9]', '', phoneme)
					newClasses[num].append(phoneme)
					newClasses[phoneme] = str(num)
					phonToSym[phoneme] = symbols[symbols.keys()[num]][0]
		print newClasses
		#get dictionary
		dictionary = {}
		for key in self.phonemes.keys():
			dictionary[key] = []
			part1 = re.sub(r'[0-9]', '', self.phonemes[key][0])
			part2 = self.phonemes[key][1]
			part3 = []
			part4 = []
			for phon in part1.split(" "):
				if phonToSym.has_key(phon):
					part3.append(phonToSym[phon])
				else:
				if newClasses.has_key(phon):
					part4.append(newClasses[phon])
				else:
					part4.append("?")
			dictionary[key].append([part1, part2, part3, part4])
		#symbolize word
		print dictionary['WORLD']
		symbolized = {}
		for word in words:
			word = word.upper()
			symbolized[word] = []
			try:
				symbolized[word].append(' '.join(dictionary[word][0][2]))
				symbolized[word].append(' '.join(dictionary[word][0][3]))
			except:
				symbolized[word].append("Not Found") 
				symbolized[word].append("")
		return symbolized
def main():
	return

if __name__ == "__main__":
	sys.exit(main())