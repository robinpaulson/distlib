from django.db import models

class User(models.Model):
	username = models.CharField(max_length=30)
	emailid = models.EmailField()
	password = models.CharField(max_length=60)
	def __str__(self):
                return self.username

class Circle(models.Model):
	circlename = models.CharField(max_length=100)
	circletype = models.CharField(max_length=20)
	def __str__(self):
                return self.circlename

class CircleUsers(models.Model):
	circle = models.ForeignKey(Circle)
	user = models.ForeignKey(User)
	
class Book(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	bookowner = models.ForeignKey(User)
	def __str__(self):
                return "%s, %s" % (self.title, self.author)
               
class Notifications(models.Model):
	fromuser = models.ForeignKey(User, related_name='notifications_fromuser')
	touser = models.ForeignKey(User, related_name='notifications_touser')
	type = models.CharField(max_length = 99)
	book = models.ForeignKey(Book)
	message = models.CharField(max_length = 3999)
	def __str__(self):
                return "from: %s, to: %s message:%s" % (self.fromuser, self.touser, self.message)
	
