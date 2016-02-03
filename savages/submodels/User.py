from __future__ import unicode_literals
from django.db import models
from UserAchieved import *
from Achievement import *

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


	# FIXME: inefficient, but given the small scale this is not too problematic
	@property
	def calculateRank(self):
		self_points = self.calculatePoints
		rank = 1

		for user in User.objects.all():
			if user.username != self.username and user.calculatePoints > self_points:
				rank += 1

		return rank