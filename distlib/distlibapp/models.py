from django.db import models

class User(models.Model):
	username = models.CharField(max_length=30)
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	emailid = models.EmailField()
	password = models.CharField(max_length=60)
	newMessages = models.IntegerField(default=0)
	def __unicode__(self):
                return unicode(self.username)
               
               

class Circle(models.Model):
	circlename = models.CharField(max_length=100)
	circletype = models.CharField(max_length=20)
	isprivate = models.BooleanField(default = True)
	def __unicode__(self):
                return unicode(self.circlename)

class CircleUsers(models.Model):
	circle = models.ForeignKey(Circle)
	user = models.ForeignKey(User)
	def __unicode__(self):
				return "%s,%s" % (self.circle, self.user)
	
class Volume(models.Model):
	title = models.CharField(max_length=100)
	authors = models.CharField(max_length=500)
	isbn10 = models.CharField(max_length=30)
	imageurl = models.CharField(max_length=200)
	def __unicode__(self):
		return "%s-%s by %s" % (self.title, self.isbn10, self.authors)
	
class Item(models.Model):
	volume = models.ForeignKey(Volume)
	bookowner = models.ForeignKey(User)
	def __unicode__(self):
		return "%s of %s" % (self.volume, self.bookowner)
               
class Notifications(models.Model):
	fromuser = models.ForeignKey(User, related_name='notifications_fromuser')
	touser = models.ForeignKey(User, related_name='notifications_touser')
	type = models.CharField(max_length = 99)
	book = models.ForeignKey(Item)
	message = models.CharField(max_length = 3999)
	def __unicode__(self):
                return "from: %s, to: %s message:%s" % (self.fromuser, self.touser, self.message)
               
class VideoTags(models.Model):
	videoId = models.CharField(max_length=20)
	tags = models.CharField(max_length=100)
	def __unicode__(self):
                return unicode(videoId)               
