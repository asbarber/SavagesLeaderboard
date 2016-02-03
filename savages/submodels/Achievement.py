from __future__ import unicode_literals
from django.db import models

class Achievement(models.Model):
	description = models.CharField(max_length=200)
	points = models.IntegerField(default=0)

	def __str__(self):
		return self.description