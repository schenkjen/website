from django.http import HttpResponse, Http404
from django.views.generic import list_detail
from sjphoto.base.models import Gallery, Photo
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

def gallery_list(request):
    
    return list_detail.object_list(request, queryset=Gallery.objects.filter(is_public=True), allow_empty=True, template_name='base/gallery_list.html' )
def gallery_detail(request, slug, obj_id):
    g = get_object_or_404(Gallery, pk=obj_id)
    return render_to_response('base/gallery_detail.html', 
                              {'gallery':g}, 
                              context_instance=RequestContext(request))