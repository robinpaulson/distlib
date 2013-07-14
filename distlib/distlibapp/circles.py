from django.db.models import Q
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import Circle
from models import CircleUsers
from models import User
from models import Volume
from models import Item
from models import Notifications
from views import books
from views import circles
from forms import LoginForm
from volumedata import VolumeData
import urllib2
import json

def circledetails(request, circlename):
    u = request.session.get('username','')
    circleobject = Circle.objects.get(circlename=circlename)
    circles = []
    circles.append(circlename)    
    users = getUsersInCircles(circles)
    ismember = False
    if u in users:
        ismember = True
        
    userobjects = User.objects.filter(username__in=users)
    items = Item.objects.filter(bookowner__in=userobjects)
    
    print "circlename " + circlename + "\n"
    print "circletype " + circleobject.circletype + "\n"
    print "userscount " + str(len(users)) + "\n"
    print "bookscount " + str(len(items)) + "\n"
    print "ismember " + str(ismember) + "\n"
    
    return render_to_response("circle.html",
        {"circlename":circlename,
         "circletype":circleobject.circletype,
         "userscount":len(users),
         "bookscount":len(items),
         "users":users,
         "ismember": ismember
     })
    

def searchcircles(request):
    u = request.session.get('username','')
    userobject = User.objects.get(username = u)
    if not u:
        return render_to_response("login.html")
    query = request.GET.get('circlename','')
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
    isprivate = request.POST.get('isprivate', False);
    
    existsAlready = False
    circleobject = Circle.objects.filter(circlename=circlename)
    
    if len(circleobject) > 0:
        existsAlready = True
        
    if existsAlready:
        return render_to_response("createcircle.html",
                                  {"error_message":"Oops, circle name taken."}
                                  )
    
    print "circlename is %s circletype is %s" % (circlename, circletype) 
    if not circlename or not circletype:
        return render_to_response("createcircle.html",
                                  )
    userobject = User.objects.get(username = u)
    if not u:
        return render_to_response("login.html")
    if circlename and circletype:
        circleobject = Circle.objects.create(circlename=circlename, circletype=circletype, isprivate=isprivate)
        circleusersobject = CircleUsers.objects.create(circle=circleobject, user=userobject)
        return (circles(request))
    else:
        return render_to_response("createcircle.html")

def addtocircle(request, circlename):
    username = request.session.get('username')
    if not username:
        return render_to_response("signup.html")
    userObject = User.objects.get(username=username)
    circleObject = Circle.objects.get(circlename=circlename)
    try:
        circleUserEntry = CircleUsers.objects.get(circle=circleObject, user=userObject)
    except CircleUsers.DoesNotExist:
        circleUserObject = CircleUsers.objects.create(circle=circleObject, user=userObject)
        circleUserObject.save()
    except:
        #do nothing
        print "swallowing exception"
    return circles(request)

def getCirclesForUserObject(userObject):
    circleusers = CircleUsers.objects.filter(user=userObject)
    circles = []
    for circleuserrow in circleusers:
        circles.append(circleuserrow.circle)
    return circles

def getUsersInCircles(circles):
    circleObjects = Circle.objects.filter(circlename__in=circles)
    circleusers = CircleUsers.objects.filter(circle__in=circleObjects).distinct()
    users = []
    for circleuser in circleusers:
        users.append(circleuser.user.username)
    return users