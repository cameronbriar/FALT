#!/usr/bin/python
#!encoding=utf-8

# The FRESNO AUDIOVISUAL LEXICON TOOL is an open source project under the MIT license.

# The MIT License (MIT)
# Copyright (c) 2012 Fresno State

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import time
import pickle
import subprocess
import Levenshtein as L
import time

# FALT : Fresno Audiovisual Lexicon Tool
# version 0.10

# this is the name of the Carnegie Melon University ARPA dictionary
# it has been modified with the IPA equivalence
# default location: /static/
defaultFilename = "cmudict_ARPA_IPA"
dictionaryWords = "words_all"
# the symbols used for representing viseme sets
# must remain in same order as symbols.keys()
symbols = {'crosshatch': [u'\u25a9', '&#9641;'], 'snowman': [u'\u2603', '&#9731;'], 'at': [u'@', '&#64;'], 'female': [u'\u2640', '&#9792;'], 'scissors': [u'\u2704', '&#9988;'], 'airplane': [u'\u2708', '&#9992;'], 'cloud': [u'\u2601', '&#9729;'], 'fourpoint': [u'\u2726', '&#10022;'], 'flower': [u'\u273f', '&#10047;'], 'phonemic': [u'\u260e', '&#9742;'], 'sun': [u'\u2742', '&#10050;'], 'peace': [u'\u270c', '&#9996;'], 'blackstar': [u'\u2738', '&#10040;'], 'elevator': [u'\u27e0', '&#10208;'], 'chess': [u'\u265a', '&#9818;'], 'smile': [u'\u263a', '&#9786;'], 'circle': [u'\u29bf', '&#10687;'], 'wheel': [u'\u2638', '&#9784;'], 'pencil': [u'\u270f', '&#9998;'], 'coffee': [u'\u2668', '&#9832;'], 'umbrella': [u'\u2602', '&#9730;'], 'perceive': [u'\u25f5', '&#9717;'], 'mac': [u'\u2318', '&#8984;'], 'eject': [u'\u23cf', '&#9167;'], 'medical': [u'\u2624', '&#9764;'], 'biohazard': [u'\u2623', '&#9763;'], 'blackdiamond': [u'\u2756', '&#10070;'], 'castle': [u'\u2656', '&#9814;'], 'star': [u'\u2605', '&#9733;'], 'sagit': [u'\u2650', '&#9808;']}

# dictionary to convert ARPA -> IPA
arpaToIPA = {'IH2': u'\u026a', 'UH0 R': u'\u028ar', 'IH1': u'\u026a', 'AH2': u'\u028c', 'AA0 R': u'\u0251r', 'AH0': u'\u0259', 'AH1': u'\u028c', 'JH': u'd\u0292', 'AW0 R': u'a\u028ar', 'EH2': u'\u025b', 'EH0': u'\u025b', 'EH1': u'\u025b', 'EY1': u'e\u026a', 'AO2 R': u'\u0254r', 'EY2': u'e\u026a', 'EH0 R': u'\u025br', 'AY1': u'a\u026a', 'IH0': u'\u026a', 'AY2': u'a\u026a', 'R0': u'\u0279', 'D': u'd', 'AO1 R': u'\u0254r', 'AW2': u'a\u028a', 'AW1': u'a\u028a', 'AW0': u'a\u028a', 'P': u'p', 'AO2': u'\u0254', 'AO1': u'\u0254', 'AO0': u'\u0254', 'AX0': u'\u028c', 'IH0 R': u'\u026ar', 'IY0 R': u'\u026ar', 'OY2': u'\u0254\u026a', 'OY1': u'\u0254\u026a', 'OY0': u'\u0254\u026a', 'UH2 R': u'\u028ar', 'UH1 R': u'\u028ar', 'UW2': u'u', 'UW1': u'u', 'UW0': u'u', 'HH': u'h', 'UH2': u'\u028a', 'UH0': u'\u028a', 'UH1': u'\u028a', 'EH1 R': u'\u025br', 'AO0 R': u'\u0254r', 'ZH': u'\u0292', 'G': u'\u0261', 'K': u'k', 'S': u's', 'IH2 R': u'\u026ar', 'W': u'w', 'ER': u'\u025d', 'AE1': u'\xe6', 'AE0': u'\xe6', 'AE2': u'\xe6', 'IH1 R': u'\u026ar', 'AW2 R': u'a\u028ar', 'EY0': u'e\u026a', 'EH2 R': u'\u025br', 'NG': u'\u014b', 'CH': u't\u0283', 'F': u'f', 'N': u'n', 'R': u'\u0279', 'V': u'v', 'Z': u'z', 'MEYE1': u'm\xe6', 'AY0': u'a\u026a', 'SH': u'\u0283', 'AW1 R': u'a\u028ar', 'DH': u'\xf0', 'IY1 R': u'\u026ar', 'B': u'b', 'DX': u'\u027e', 'AA1 R': u'\u0251r', 'AA2 R': u'\u0251r', 'TH': u'\u03b8', 'AA1': u'\u0251', 'IY0': u'i', 'IY2': u'i', 'M': u'm', 'L': u'l', 'IH': u'\u026a', 'IY2 R': u'\u026ar', 'Y': u'j', 'OW1': u'o\u028a', 'OW0': u'o\u028a', 'OW2': u'o\u028a', 'ER0': u'\u025d', 'ER1': u'\u025a', 'ER2': u'\u025a', 'IY1': u'i', 'AA0': u'\u0251', 'AA2': u'\u0251', 'T': u't'}

# dictionary to convert IPA -> ARPA
ipaToARPA = {u'\u0283': ['SH'], u'a\u028a': ['AW1', 'AW0', 'AW2'], u'o\u028a': ['OW1', 'OW0', 'OW2'], u'e\u026a': ['EY1', 'EY0', 'EY2'], u'a\u028ar': ['AW0 R', 'AW2 R', 'AW1 R'], u'a\u026a': ['AY1', 'AY0', 'AY2'], u'\u0254r': ['AO1 R', 'AO0 R', 'AO2 R'], u'\u028c': ['AH2', 'AH1', 'AX0'], u'\u0292': ['ZH'], u'\u0254\u026a': ['OY2', 'OY1', 'OY0'], u'\u025br': ['EH0 R', 'EH1 R', 'EH2 R'], u'\xf0': ['DH'], u'j': ['Y'], u'\u03b8': ['TH'], u'b': ['B'], u'd\u0292': ['JH'], u'\u0251r': ['AA0 R', 'AA1 R', 'AA2 R'], u'\u014b': ['NG'], u'\u026ar': ['IH0 R', 'IY0 R', 'IH2 R', 'IH1 R', 'IY1 R', 'IY2 R'], u'\u0251': ['AA0', 'AA2', 'AA1'], u'm\xe6': ['MEYE1'], u'\u0254': ['AO2', 'AO1', 'AO0'], u'\u0259': ['AH0'], u'\u025b': ['EH2', 'EH0', 'EH1'], u'\u025a': ['ER1', 'ER2'], u'\u025d': ['ER', 'ER0'], u't\u0283': ['CH'], u'\u0261': ['G'], u'f': ['F'], u'd': ['D'], u'\xe6': ['AE1', 'AE0', 'AE2'], u'i': ['IY1', 'IY0', 'IY2'], u'h': ['HH'], u'k': ['K'], u'\u026a': ['IH2', 'IH2', 'IH1', 'IH0', 'IH'], u'm': ['M'], u'l': ['L'], u'\u028ar': ['UH0 R', 'UH0 R', 'UH2 R', 'UH1 R'], u'n': ['N'], u'r': ['R'], u'\u028a': ['UH2', 'UH0', 'UH1'], u'p': ['P'], u's': ['S'], u'u': ['UW2', 'UW1', 'UW0'], u't': ['T'], u'w': ['W'], u'v': ['V'], u'\u0279': ['R0', 'R'], u'z': ['Z'], u'\u027e': ['DX']}

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
		self.dictWords = open(dictionaryWords)
		self.dictionary = pickle.load(self.dictWords)
		self.dictWords.close()
		self.phonemes = self.getDictionary()
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

		if self.phonemes.has_key(word):
			self.result.append(word)
			self.result.append(self.phonemes[word][0])
			self.result.append(self.phonemes[word][1])
	   	# if there is no exact match, try a rough match
	   	else:
	   		p = subprocess.Popen("grep -i --line-buffered '"+word+"' "+filename, shell=True, stdout=subprocess.PIPE)
	   		self.result = p.communicate(None)[0].split("\n")[0].split("  ")

	   	if self.result == ['']:
	   		self.result = [word, '', '']
	   	# resul = [ word , ARPA, IPA ]
   		return self.result

   	def getIndex(self, size):
   		d = { 1 : 0, 2 : 1, 10 : 2, 12 : 3, 19 : 4, 28 : 5 }
   		return d[size]

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
   		index = self.getIndex(size)
   		# if there was not entry for the word
   		if info[1] == '':
   			return ['<small>Not found.</small>', '', '', '', '']

   		symbolized = self.dictionary[info[0]][-1][index]
   		visemeSet = self.dictionary[info[0]][index]

   		print info[0], info[1], info[2]
   		# [symbolized version, original word, arpa, ipa, viseme classes]
   		return [symbolized, info[0], info[1], info[2], visemeSet]

   	def getSimilarities(self, word, size, maxDistance=1):
   		#index : { 0 : 1, 1 : 2, 2 : 10, 3 : 12, 4 : 19, 5 : 28 }
   		if word == '':
   			return []
   		similar = []
   		total = 0
   		index = self.getIndex(size)
   		word = word.upper()
   		for eachWord in self.dictionary:
   			if abs(len(self.dictionary[word][-1][index]) - len(self.dictionary[eachWord][-1][index])) > 0:
   				continue
   			else:
   				try:
					if L.distance(''.join(self.dictionary[eachWord][-1][index]), ''.join(self.dictionary[word][-1][index])) <= maxDistance:
						similar.append((eachWord, ''.join(self.dictionary[eachWord][-1][index])))
						total += 1
				except:
					continue
   		return similar

	def getFamiliarity(self, word):
		# reference WordNet for word familiarity
		# return the highest familiarity, -1 for not found
		highestFaml = -1
		for wordType in ['n', 'v', 'a', 'r']:
			process = "wn '"+word+"' -faml"+wordType
			p = subprocess.Popen(process, shell=True, stdout=subprocess.PIPE)
			try:
				result = p.communicate()[0].split("\n")[3][-2][0]
				if int(result) > int(highestFaml):
					highestFaml = result
			except:
				continue
		return highestFaml


def main():
	return

if __name__ == "__main__":
	sys.exit(main())