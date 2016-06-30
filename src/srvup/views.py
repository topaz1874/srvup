from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from video.models import Video

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

