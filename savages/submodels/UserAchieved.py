from __future__ import unicode_literals
from django.db import models

class UserAchieved(models.Model):
	userId = models.IntegerField(default=0)
	achievementId = models.IntegerField(default=0)

	def __str__(self):
		return self.userId + self.achievementId