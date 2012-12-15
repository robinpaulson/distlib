from django.db.models import Q
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import Circle
from models import CircleUsers
from models import User
from models import Volume
from models import Item
from models import Notifications
from forms import LoginForm
from views import books
from circles import getCirclesForUserObject
from circles import getUsersInCircles
from users import getItemsForUsers
from volumedata import VolumeData
import urllib2
import json

def searchbooks(request):
    ''' Searches for books in the users circles '''
    
    u = request.session.get('username', '')
    print "u is %s"  % u
    userobject = User.objects.get(username=u)
    if not u:
        return render_to_response("login.html")
    query = request.GET.get('q','')
    
    circles = getCirclesForUserObject(userobject)
    users = getUsersInCircles(circles)
    items = getItemsForUsers(users)

    shortlistedItems = []
    for item in items:
        if query.lower() in item.volume.title.lower():
            shortlistedItems.append(item)
    return render_to_response("search.html", {
        "results": shortlistedItems,
        "query": query,
        "resulttype": "books",
})
        
        
def addbook(request):
    u = request.session.get('username', '')
    userobject = User.objects.get(username=u)
    if not u:
        return render_to_response("signup.html")
    
    title = request.POST.get('title','')
    
    googlebooksurl = 'https://www.googleapis.com/books/v1/volumes?q=%s&key=AIzaSyAh9amDouy8_zI-teUcigYfYkisrXYOc1s' % urllib2.quote(title)
    response = urllib2.urlopen(googlebooksurl)
    content = response.read()
    
    json_object = json.loads(content)
    
    bookvolumes = []
    isbn10s = []
    for volume in json_object["items"]:
        x = volume["volumeInfo"]
        title = ""
        authors = []
        thumbnail = ""
        isbn10 = ""
        if "title" in x:
            title = x["title"]
        if "authors" in x:
            authors = x["authors"]
        if "imageLinks" in x:
            imageLinks = x["imageLinks"]
            if "thumbnail" in imageLinks:
                thumbnail = imageLinks["smallThumbnail"]
        if "industryIdentifiers" in x:
            for object in x["industryIdentifiers"]:
                if object["type"] == "ISBN_10":
                    isbn10 = object["identifier"]
        
        if isbn10 in isbn10s:
            continue
        else:
            isbn10s.append(isbn10)
            
        authorsString = ""
        first = True
        for author in authors:
            if first == False:
                authorsString += ","
                first = False
            authorsString += author
        
        volume = ""
        existingVolumes = Volume.objects.filter(isbn10 = isbn10)
        if not existingVolumes:
            volume = Volume.objects.create(title=title, authors=authorsString, isbn10=isbn10, imageurl=thumbnail)
            volume.save()
        else:
            volume = existingVolumes[0]
        
        bookvolumes.append(volume)
        
    print bookvolumes
    return render_to_response("addbooks.html",{
                                               "bookvolumes": bookvolumes[0:9]
                                               })
                                               
    return (books(request))


def addvolume(request, isbn10):
    ''' Add the given isbn10 based volume to user's shelf '''
    
    u = request.session.get('username', '')
    if not u:
        return render_to_response("signup.html")
    userobject = User.objects.get(username=u)
    
    volume = Volume.objects.get(isbn10=isbn10)

    try:
        item = Item.objects.get(volume=volume, bookowner=userobject)
    except Item.DoesNotExist:
        item = Item.objects.create(volume = volume, bookowner=userobject)
        item.save()
    except:
        #do nothing
        print "swallowing exception"
        
    return books(request)