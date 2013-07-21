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
from django.utils.datetime_safe import datetime

def books(request):
    userobject = request.session.get('userobject');
    if not userobject:
        print "NO USER OBJECT !!!!!!!!!!!!!!!!!!"
        return render_to_response("login.html")
    else:
        items = Item.objects.filter(bookowner = userobject)
        books = []
        for item in items:
            books.append(item.volume)

    return render_to_response("books.html", {
            "user": userobject,
            "books": books,
            })
    
def circles(request):
    userobject = request.session.get('userobject');
    if not userobject:
        return render_to_response("login.html")
    else:
        usersCircles = []
        circleUsers = CircleUsers.objects.filter(user=userobject)
        for circleUserRow in circleUsers:
            usersCircles.append(circleUserRow.circle)
        return render_to_response("circles.html", {
            "user": userobject,
            "circles": usersCircles
            })

def notifications(request):
    userobject = request.session.get('userobject') 
    username = request.session.get('username')
    if not userobject:
        return render_to_response("login.html")
    else:
        #userobject.newMessages = 0;
        #userobject.save();
        request.session['userobject'] = userobject
        notifications = Notifications.objects.filter(Q(touser=userobject) | Q(fromuser=userobject))
        print "user is " + username
        return render_to_response("notifications.html", {
            "username": username,
            "user": userobject,
            "notifications": notifications
            })

def login(request):
    form = LoginForm()
    return render_to_response('login.html', {'form': form})

def logout(request):
    del request.session['username']
    del request.session['userobject']
    return login(request)

def authenticate(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username:
        userobject = User.objects.filter(username=username)
        if not userobject:
            return render_to_response("signup.html")
        else:
            request.session['username'] = username
            request.session['userobject'] = userobject
            return(books(request))
    else:
        return render_to_response("login.html",{'form': LoginForm()})

def signup(request):
    username = request.POST.get('username')
    if not username:
        return render_to_response("signup.html")
    firstname = request.POST.get('firstname')
    if not firstname:
        return render_to_response("signup.html")
    lastname = request.POST.get('lastname')
    if not lastname:
        return render_to_response("signup.html")
    password = request.POST.get('password')
    if not password:
        return render_to_response("signup.html")
    emailid = request.POST.get('email')
    if not emailid:
        return render_to_response("signup.html")

    userobject = User.objects.create(username=username, password=password, emailid=emailid)
    request.session['username'] = username
    request.session['userobject'] = userobject

    return books(request)
    
def ask(request, user, isbn):
    username = request.session.get('username')
    if not username:
        return render_to_response("signup.html")
    volume = Volume.objects.get(isbn10 = isbn)
    return render_to_response("ask.html",{
                                          "to": user,
                                          "title": volume.title,
                                          "isbn": volume.isbn10
    })
    
def asked(request, touser, isbn):
    username = request.session.get('username')
    fromuserobject = User.objects.get(username = username)
    if not username:
        return render_to_response("signup.html")
    touserobject = User.objects.get(username = touser)
    type = "ask"
    book = Volume.objects.get(isbn10=isbn)
    item = Item.objects.get(volume=book, bookowner=touserobject)
    message = request.POST.get('message')
    print message
    notificationobject = Notifications.objects.create(fromuser=fromuserobject, touser=touserobject, book=item, message=message, type= type)    
    return books(request)