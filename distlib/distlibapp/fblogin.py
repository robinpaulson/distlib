import urllib
import urllib2
import re
import json
from django.http import HttpResponseRedirect
from models import User
from views import books

def fblogin(request):
    
    codeobject = request.GET.get('code')
    if(codeobject is None):
        parameters = {}
        parameters['client_id'] = '377058139053021'
        parameters['redirect_uri'] = 'http://www.dronesclub.in/fblogin'
        parameters['state'] = 'whatho'
        parameters['scope'] = 'user_birthday,read_stream'
        
        parametersString = urllib.urlencode(parameters)  

        urlstring = "https://www.facebook.com/dialog/oauth?" + parametersString
        print "URLSTRING is " + urlstring
        return HttpResponseRedirect(urlstring)
    
    else:
        
        #exchange the code for an access token
        
        parameters = {}
        parameters['client_id'] = '377058139053021'
        parameters['redirect_uri'] = 'http://www.dronesclub.in/fblogin'
        parameters['client_secret'] = '44fc382d9399610f1eaccd153ba9083c'
        parameters['code'] = codeobject
        
        parametersString = urllib.urlencode(parameters)
        
        urlstring = "https://graph.facebook.com/oauth/access_token?" + parametersString
        
        response = urllib2.urlopen(urlstring)
        
        content = response.read()
        contentPattern = re.compile(r'access_token=(.*?)&expires=.*')
        accessToken = contentPattern.search(content).groups()[0]
        
        urlstring = 'https://graph.facebook.com/me?access_token=' + accessToken
        userDetailsJson = urllib2.urlopen(urlstring)
        fb_response = userDetailsJson.read()
        json_object = json.loads(fb_response)
        
        username = 'fb_' + json_object['id']
        password = username
        emailid = json_object['username'] + '@facebook.com'
        
        userobject = User.objects.create(username=username, password=password, emailid=emailid)
        request.session['username'] = username
        request.session['userobject'] = userobject

        return books(request)