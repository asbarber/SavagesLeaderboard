from __future__ import unicode_literals
from django.db import models
from UserAchieved import *

class User(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	name = models.CharField(max_length=40)

	@property
	def calculatePoints(self):
		link_list = UserAchieved.objects.filter(userId = self.id)
		num_points = 0
		for link in link_list:
			achievement_list = Achievement.objects.filter(id = link.achievementId)
			achievement = achievement_list[0]
			num_points += achievement.points
		return num_points

	def __str__(self):
		return self.username