from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseRedirect
from django.template.context import RequestContext
from sjphoto.base.models import PhotoContest, Photo
from sjutils.utils import get_admin_object, get_object
from django.contrib.contenttypes.models import ContentType
from likeables.models import Likeable

def photo_contest_detail(request,slug, ct_id, obj_id):
    contest = get_object(ct_id, obj_id, depth=2)
    
    return render_to_response('base/contest_detail.html', {'contest':contest}, context_instance=RequestContext(request))

def get_photocontest_winner(request, slug, obj_id):
    
    photos = PhotoContest.objects.get(pk=obj_id).photos.values_list('id', flat=True)
    p_ct = ContentType.objects.get_for_model(Photo)
    winner = Likeable.objects.filter(content_type=p_ct, object_id__in=photos).order_by('-likes')[0]
    return HttpResponse()
