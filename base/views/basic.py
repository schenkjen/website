# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.db.models import Q
from sjphoto.base.models import Gallery
from sjphoto.forms.models import MultiComposeForm
from messages.views import compose
from sjphoto.base.forms.models import LoginForm

def home_page(request, slug=None, obj_id=None):
    
    if obj_id is None:
        gList = Gallery.featured.select_related(depth=3)
        return render_to_response('base/home.html', {'gallery':gList.latest(),'gallery_list':gList[:3]}, context_instance=RequestContext(request))
    else:
        gList = Gallery.objects.select_related(depth=3)
        return render_to_response('base/home.html', {'gallery':gList.get(pk=obj_id),'gallery_list':gList[:3]}, context_instance=RequestContext(request))
def gallery_view(request, slug):
    import pdb
    pdb.set_trace()
    g = None
    gl = Gallery.objects.filter.all()
    try:
        g = gl.get(title_slug__exact = slug)
    except ObjectDoesNotExist:
        raise Http404
    return render_to_response('base/home.html', {
                                                 'gallery':g, 
                                                 'gallery_list':FeatureGallery.objects.select_related(depth=3).all()[:3]},
                                                 context_instance=RequestContext(request))
def login_user(request, next='/'):

    #message = None
    if request.is_ajax():
        pass
    else:
    	if request.POST:
			login_form = LoginForm(request.POST, initial={'next':next})
			if login_form.is_valid():
				u = login_form.cleaned_data['username']
				p = login_form.cleaned_data['password']
				the_user = authenticate(username=u, password=p)
				if the_user is not None and the_user.is_active:
					login(request, the_user)
					if request.GET:
						redir = request.GET['next']
					else:
						redir = '/'
					return HttpResponseRedirect(redir)
				else:
					message = "password and username did not match"
					form = LoginForm(request.POST, initial={'next':next})
					return render_to_response('base/login.html', {'form':form}, context_instance=RequestContext(request))
        else:
			login_form = LoginForm(initial={'next':request.META.get('HTTP_REFERER') or '/'})
			return render_to_response('base/login.html', {'form':login_form}, context_instance=RequestContext(request))

def logout_user(request):
    '''log out the user and redirect to home page'''
    logout(request)
    return HttpResponseRedirect('/')

def multi_compose(request):
    '''replace standard compose form with the autocompleter form'''
    return compose(request, form_class=MultiComposeForm, template_name='messages/multicompose.html')
def user_search(request):
	search = request.POST['search']
	if " " in search:
		fname, lname = search.split(" ")
	else:
		fname = lname = None
	if fname and lname:
		p1 = Q(user__first_name__icontains=fname)
		p2 = Q(user__last_name__icontains=lname)
		result = User.objects.filter(p1 & p2)
	else:
		p1 = Q(first_name__icontains=search)
		p2 = Q(last_name__icontains=search)
		p3 = Q(username__icontains=search)
		result = User.objects.filter(p1 | p2 | p3)
	if not request.user.is_staff:
            result = result.filter(is_staff = True)
        result = result[:10]
	return HttpResponse(simplejson.dumps([dict(username=u.username,
											   name=u.get_full_name(),
											   ct_id=ContentType.objects.get_for_model(u).pk,
											   obj_id=u.pk) for u in result]), mimetype='application/javasctipt')

