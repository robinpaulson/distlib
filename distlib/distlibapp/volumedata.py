class VolumeData:
	def __init__(self, title, authors, imageurl, isbn10):
		self.title = title
		self.authors = authors
		self.imageurl = imageurl
		self.isbn10 = isbn10
		
	def __str__(self):
    		return "%s, %s, %s, %s, %s" % (self.title, self.authors, self.imageurl, self.isbn10, self.isbn13)