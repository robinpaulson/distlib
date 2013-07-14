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
from volumedata import VolumeData
import urllib2
import json

def userdetails(request, username):
    userobject = User.objects.get(username=username)
    books = []
    items = Item.objects.filter(bookowner=userobject)
    for item in items:
        books.append(item.volume)
    circleusers = CircleUsers.objects.filter(user=userobject)
    circles = []
    for circleuserrow in circleusers:
        circles.append(circleuserrow.circle)
    return render_to_response("user.html",
                                  {"user":userobject,
                                   "books": books,
                                   "circles":circles
                                   })
def searchUsers(query):
    results = []
    if query:
        results = User.objects.filter(username__icontains=query).distinct()
    return results
        
def getItemsForUsers(users):
    outerItems = Item.objects.filter(bookowner__in=users).distinct()
    items = []
    for outerItem in outerItems:
        items.append(outerItem)
    return items
