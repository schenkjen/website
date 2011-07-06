from PIL import Image
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.defaultfilters import date, slugify
from django.utils import simplejson
from sjphoto.base.models import Photo
from sjphoto.base.forms.models import LoginForm, PhotoUploader

def photo_upload(request):
    if request.FILES:

        form = PhotoUploader(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            bits = photo.image_filename().split('.')
            ext = bits[-1].lower()
            photo.title = bits[0].replace('_', '-').replace('-', ' ').capitalize()
            photo.title_slug = slugify(photo.title)
            photo.save()
            s = photo.get_display_size()
            return HttpResponse(simplejson.dumps({'status':1,
                                                  'width':s[0],
                                                  'height':s[1],
                                                  'mime':ext,
                                                  'preview':photo.get_admin_thumbnail_url()}
            ), mimetype="text/javascript")
    else:
        f = PhotoUploader()
        return render_to_response('fancyupload.html', {'form':f}, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':1}), mimetype="text/javascript")

def get_exif(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    exif = photo.EXIF
    width = exif.get('EXIF ExifImageWidth', None)
    height = exif.get('EXIF ExifImageHeight', None)
    
    if width is None:
        im = Image.open(photo.image.path)
        width, height = im.size
        
    data = {'exposureTime':"%s sec" % exif.get('EXIF ExposureTime', 'unknown'),
            'imageModel':"%s" % exif.get('Image Model', 'unknown'),
            'focalLength':"%s mm" % exif.get('EXIF FocalLength', 'unknown'),
            'flash':"%s" % exif.get('EXIF Flash', 'unknown'),
            'resolution':"%s x %s" % (width, height),
            'dateTaken':date(photo.date_taken, "b dS Y"),
            'title':photo.title}

    return HttpResponse(simplejson.dumps(data), mimetype="text/javascript")

def ajax_login(request):
    # POSTs done by Request.JSON
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # we have a winner
            if user is not None and user.is_active:
                auth.login(request, user)
                try:
                    #p =  user.get_profile()
                    return HttpResponse(simplejson.dumps({'user':True, 'location':request.META['HTTP_REFERER']}), mimetype="application/javascript")
                except:
                    return HttpResponse(simplejson.dumps({'user':True, 'location':user.get_profile().get_absolute_url()}), mimetype="application/javascript")
            else:
                return HttpResponse(simplejson.dumps({'user':False, 'msg':"Username & Password do not match"}), mimetype="application/javascript")

        else:
            return HttpResponse(simplejson.dumps({'user':False, 'msg':"Username & Password do not match"}), mimetype="application/javascript")
    # GETs done by Request.HTML
    else:
        form = LoginForm()
        return HttpResponse(form.as_ul())