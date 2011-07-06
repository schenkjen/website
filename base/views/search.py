from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType
from djapian.indexer import CompositeIndexer, Indexer
from overexposure.models import Entry
from operator import itemgetter
from sjphoto.base.models import Photo, Gallery

try:
    import xapian
except ImportError:
    xapian = None
    
def photo_search(request):
    if request.is_ajax():
        if request.POST:
            photos = Photo.objects.filter(title__icontains=request.POST['search'])[:10]
            return HttpResponse(simplejson.dumps([dict(title=p.title,
                                                       obj_id=p.pk,
                                                       preview=p.get_search_url(),
                                                       image=p.get_blog_url()) for p in photos]), mimetype="text/javascript")

    else:
        return HttpResponseForbidden()

def ajax_main_search(request):
    if xapian is None:
        result = []
        return HttpResponse(simplejson.dumps(result, mimetype="text/javascript"))
    if request.is_ajax():
        if request.POST:
            try:
                search = request.POST['searchVal']
                if " " in search:
                    search = search.replace(" ", " OR ")
                if "." in search:
                    search = search.replace(".", ' AND ')
                flags = xapian.QueryParser.FLAG_PARTIAL | xapian.QueryParser.FLAG_WILDCARD \
                    | xapian.QueryParser.FLAG_BOOLEAN | xapian.QueryParser.FLAG_PHRASE
                    
                indexers = [Entry.indexer, Gallery.indexer]
                
                comp = CompositeIndexer(*indexers)
                res = comp.search(search).flags(flags)
                rlist = [dict(name=x.instance.__unicode__(),
                              ct_id=ContentType.objects.get_for_model(x.instance).pk,
                              ct=ContentType.objects.get_for_model(x.instance).name,
                              obj_id=x.instance.pk,
                              displayname=x.instance.title,
                              url=x.instance.get_absolute_url() or None) for x in res]
                return HttpResponse(simplejson.dumps(rlist),
                                mimetype='text/javascript')
            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponse(simplejson.dumps({'error':True}, mimetype="text/javascript"))
    else:
        # can probably change to redirect to a search
        # page view as well
        return HttpResponseBadRequest()
