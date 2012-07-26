import FALT as F
import re
from pygame import mixer
import pickle

mixer.init()
alert = mixer.Sound('/Users/cameronbriar/Desktop/boom.wav')

infil = 'cmudict_words'
allWords = open(infil)

outfilname = 'words_symbolized_'
sizes = [1,2,10,12,19,28]

d = {}
print 'started'

#alert.play()
for i, size in enumerate(sizes):
	f = F.FALT(size)
	for word in allWords:
		word = re.sub("[^a-zA-Z]", "", word)
		if d.has_key(word):
			if len(d[word]) <= i:
				d[word].append(' '.join(str(x+1) for x in f.symbolize(word)[4]))
		else:
			d[word] = []
			d[word].append(' '.join(str(x+1) for x in f.symbolize(word)[4]))
		print word[0]+word[1]+" "+d[word]
	allWords.close()
	allWords = open(infil)
#alert.play()
print 'complete'

ofil = open(outfilname, 'w')
pickle.dump(d, ofil)
ofil.close()
print 'done'