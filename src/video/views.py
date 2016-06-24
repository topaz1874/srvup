from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Video,Category

@login_required
def video_detail(request,cat_slug,vid_slug):
    try:
        cat = Category.objects.get(slug=cat_slug)
    except:
        return Http404
    try:
        obj = Video.objects.get(slug=vid_slug, category=cat)
        return render(request, 'video/video_detail.html', {'object':obj})
    except:
        return Http404

def category_list(request):
    queryset = Category.objects.all()
    return render(request, 'video/category_list.html', {'queryset':queryset,})

@login_required
def category_detail(request, cat_slug):
    try:
        cat = Category.objects.get(slug=cat_slug)
        return render(request, 'video/category_detail.html', {'object': cat,})
    except:
        return Http404
