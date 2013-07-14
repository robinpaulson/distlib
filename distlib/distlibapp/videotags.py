from models import VideoTags
from django.http import HttpResponse

def getVideoTags(request):
    id = request.GET.get('id','')
    videoTagsObject = VideoTags.objects.get(videoId=id)
    response = HttpResponse(videoTagsObject.tags)
    return response
    
def putVideoTags(request):
    id = request.GET.get('id','')
    millis = request.GET.get('millis','')
    asin = request.GET.get('asin','')
    tagString = "%s:%s" % (millis, asin)
    try:
        videoTagsObject = VideoTags.objects.get(videoId=id)
    except VideoTags.DoesNotExist: 
        videoTagsObjectNew = VideoTags.objects.create(videoId=id, tags=tagString)
        videoTagsObjectNew.save()
        response = HttpResponse(videoTagsObjectNew.tags)
    else:
        tagStringWithCommaPrefix = ",%s" % (tagString)
        videoTagsObject.tags += tagStringWithCommaPrefix
        videoTagsObject.save()
        response = HttpResponse(videoTagsObject.tags)
    return response