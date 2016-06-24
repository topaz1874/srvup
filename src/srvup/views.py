from django.contrib.auth import authenticate,login,logout
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponseRedirect
from video.models import Video
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
# @login_required(login_url='/enroll/login')
@login_required
def home(request):
    name = "Justin"
    videos = Video.objects.all()
    embeds = []
    for vid in videos:
        code = mark_safe(vid.embed_code)
        embeds.append("%s"%(code))


    context = {
		"the_name": name,
		"videos": videos,
        "numbers": videos.count(),
        "the_embeds":embeds,

	}
    return render(request, "home.html", context)

@login_required(login_url='/login/')
def staff_home(request):
    return render(request, 'home.html', context={})

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
def auth_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # print request.GET.get('next')
            return HttpResponseRedirect(request.GET.get('next'))
    context = {
        'form': form
    }
    return render(request, 'login.html' ,context)