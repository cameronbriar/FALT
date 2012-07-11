from django.db import models

# Create your models here.
class Word(models.Model):
	word = models.CharField(max_length=100)
	arpa = models.CharField(max_length=100)
	ipa = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.word
