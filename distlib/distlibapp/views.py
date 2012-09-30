from django.db.models import Q
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import Book
from models import Circle
from models import CircleUsers
from models import User
from models import User
from models import Notifications
from forms import LoginForm
from volumedata import VolumeData
import urllib2
import json

def searchbooks(request):
    u = request.session.get('username', '')
    print "u is %s"  % u
    userobject = User.objects.get(username=u)
    print type(userobject)
    if not u:
        return render_to_response("login.html")
    query = request.GET.get('q','')
    circleusers = CircleUsers.objects.filter(user=userobject)
    circles = []
    for circleuserrow in circleusers:
        circles.append(circleuserrow.circle)
    print circles
    users = CircleUsers.objects.filter(circle__in=circles).distinct()
    for user in users:
        for circleuser in circleusers:
            if user == circleuser.user:
                usercirclemap[user] = circleuser.circle
    print users
    books = Book.objects.filter(bookowner__in=users).filter(title__icontains=query).distinct()
        
    print books

    return render_to_response("search.html", {
        "results": books,
        "query": query,
        "resulttype": "books",
})
    
def circledetails(request, circlename):
    circleobject = Circle.objects.get(circlename=circlename)
    circleusers = CircleUsers.objects.filter(circle=circleobject)
    usernames = []
    userobjects = []
    for circleuser in circleusers:
        usernames.append(circleuser.user.username)
        userobjects.append(User.objects.get(username=circleuser.user.username))
    print usernames
    books = Book.objects.filter(bookowner__in=userobjects)
    print books
    
    return render_to_response("circle.html",
        {"circlename":circlename,
         "circletype":circleobject.circletype,
         "userscount":circleusers.count(),
         "bookscount":books.count(),
         "users":usernames
     })
    
def userdetails(request, username):
    userobject = User.objects.get(username=username)
    books = Book.objects.filter(bookowner=userobject)
    circleusers = CircleUsers.objects.filter(user=userobject)
    circles = []
    for circleuserrow in circleusers:
        circles.append(circleuserrow.circle)
    return render_to_response("user.html",
                                  {"user":userobject,
                                   "books": books,
                                   "circles":circles
                                   })
    
def searchcircles(request):
    u = request.session.get('username','')
    userobject = User.objects.get(username = u)
    if not u:
        return render_to_response("login.html")
    query = request.GET.get('q','')
    if query:
        results = Circle.objects.filter(circlename__icontains=query).distinct()
    else:
        results = []
        
    return render_to_response("search.html",{
              "results": results,
              "query": query,
              "resulttype": "circles",
}) 
    
def createcircle(request):
    u = request.session.get('username','')
    circlename = request.POST.get('circlename','')
    circletype = request.POST.get('circletype','')
    
    print "circlename is %s circletype is %s" % (circlename, circletype) 
    if not circlename:
        return render_to_response("createcircle.html",
                                  {"error_message":"circle name invalid"})
    if not circletype:
        return render_to_response("createcircle.html",
                                  {"error_message":"circle name invalid"})
    userobject = User.objects.get(username = u)
    if not u:
        return render_to_response("login.html")
    if circlename and circletype:
        circleobject = Circle.objects.create(circlename=circlename, circletype=circletype)
        circleusersobject = CircleUsers.objects.create(circle=circleobject, user=userobject)
        return (home(request))
    else:
        return render_to_response("createcircle.html")
    
def home(request):
    return books(request)

def books(request):
    userobject = request.session.get('userobject');
    if not userobject:
        return render_to_response("login.html")
    else:
        books = Book.objects.filter(bookowner = userobject)
        usersCircles = []
        circleUsers = CircleUsers.objects.filter(user=userobject)
        notifications = Notifications.objects.filter(touser=userobject)
        for circleUserRow in circleUsers:
            usersCircles.append(circleUserRow.circle)
        return render_to_response("books.html", {
            "user": userobject,
            "books": books,
            "circles": usersCircles,
            "notifications": notifications
            })
        
def circles(request):
    userobject = request.session.get('userobject');
    if not userobject:
        return render_to_response("login.html")
    else:
        books = Book.objects.filter(bookowner = userobject)
        usersCircles = []
        circleUsers = CircleUsers.objects.filter(user=userobject)
        notifications = Notifications.objects.filter(touser=userobject)
        for circleUserRow in circleUsers:
            usersCircles.append(circleUserRow.circle)
        return render_to_response("circles.html", {
            "user": userobject,
            "books": books,
            "circles": usersCircles,
            "notifications": notifications
            })

def notifications(request):
    userobject = request.session.get('userobject');
    if not userobject:
        return render_to_response("login.html")
    else:
        books = Book.objects.filter(bookowner = userobject)
        usersCircles = []
        circleUsers = CircleUsers.objects.filter(user=userobject)
        notifications = Notifications.objects.filter(touser=userobject)
        for circleUserRow in circleUsers:
            usersCircles.append(circleUserRow.circle)
        return render_to_response("notifications.html", {
            "user": userobject,
            "books": books,
            "circles": usersCircles,
            "notifications": notifications
            })
        
def searches(request):
    userobject = request.session.get('userobject');
    if not userobject:
        return render_to_response("login.html")
    else:
        books = Book.objects.filter(bookowner = userobject)
        usersCircles = []
        circleUsers = CircleUsers.objects.filter(user=userobject)
        notifications = Notifications.objects.filter(touser=userobject)
        for circleUserRow in circleUsers:
            usersCircles.append(circleUserRow.circle)
        return render_to_response("searches.html", {
            "user": userobject,
            "books": books,
            "circles": usersCircles,
            "notifications": notifications
            })
        
def about(request):
    return render_to_response('about.html')
    

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
            return(home(request))
    else:
        return render_to_response("login.html",{'form': LoginForm()})

def addbook(request):
    u = request.session.get('username', '')
    userobject = User.objects.get(username=u)
    if not u:
        return render_to_response("signup.html")
    book = Book(title="", author="")
    book.title = request.POST.get('title','')
    book.author = request.POST.get('author','')
    
    googlebooksurl = 'https://www.googleapis.com/books/v1/volumes?q=%s&key=AIzaSyAh9amDouy8_zI-teUcigYfYkisrXYOc1s' % urllib2.quote(book.title)
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
        
        bookvolume = VolumeData(title, authors, thumbnail, isbn10)
        bookvolumes.append(bookvolume)
        
    print bookvolumes
    return render_to_response("addbooks.html",{
                                               "bookvolumes": bookvolumes[0:6]
                                               })
                                               
    return (home(request))

def signup(request):
    username = request.POST.get('username')
    if not username:
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

    return home(request)

def addtocircle(request, circlename):
    username = request.session.get('username')
    if not username:
        return render_to_response("signup.html")
    userobject = User.objects.get(username=username)
    circleobject = Circle.objects.get(circlename=circlename)
    circleusersobject = CircleUsers.objects.create(circle=circleobject, user=userobject)
    
    return home(request)
    
def ask(request, user, bookname):
    username = request.session.get('username')
    if not username:
        return render_to_response("signup.html")
    return render_to_response("ask.html",{
                                          "to": user,
                                          "title": bookname
    })
    
def asked(request, touser, bookname):
    username = request.session.get('username')
    fromuserobject = User.objects.get(username = username)
    if not username:
        return render_to_response("signup.html")
    touserobject = User.objects.get(username = touser)
    type = "ask"
    book = Book.objects.get(title=bookname, bookowner=touserobject)
    message = request.POST.get('message')
    print message
    notificationobject = Notifications.objects.create(fromuser=fromuserobject, touser=touserobject, book=book, message=message, type= type)    
    return home(request)
    
