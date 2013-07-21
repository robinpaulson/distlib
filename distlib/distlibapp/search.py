from django.db.models import Q
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from circles import searchCircles1
from books import searchBooks
from users import searchUsers
import urllib2
import json
from django.utils.datetime_safe import datetime

def search(request):
    userobject = request.session.get('userobject');
    if not userobject:
        print "NO USER OBJECT !!!!!!!!!!!!!!!!!!"
        return render_to_response("login.html")
    else:
        term = request.GET.get('q')
        print "term is " + term
        books = searchBooks(term)
        users = searchUsers(term)
        circles = searchCircles1(term)
        
        totalLen = len(books) + len(users) + len(circles)

    return render_to_response("search.html", {
            "users": users,
            "books": books,
            "circles": circles,
            "len":totalLen,
            })