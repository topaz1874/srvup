from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Video,Category
from comment.forms import CommentForm
from analytics.signals import page_view

@login_required
def like_video(request):
    vid_id = None
    if request.method == 'GET':
        vid_id = request.GET['video_id']
        likes = 0
        if vid_id:
            vid = Video.objects.get(id=int(vid_id))
            likes = vid.likes + 1
            vid.likes = likes
            vid.save()
    return HttpResponse(likes)


# @login_required
def video_detail(request,cat_slug,vid_slug):
    """
    video object can be retrieved if user is authenticated 
    or has free preivew property otherwise redirect to login
    page
    """
    cat = get_object_or_404(Category, slug=cat_slug)
    obj = get_object_or_404(Video, category=cat, slug=vid_slug)
    
    page_view.send(
        sender = request.user,
        path = request.get_full_path(),
        primary_obj = obj,
        secondary_obj = cat)


    if request.user.is_authenticated():
        member = request.user.is_member
        if member:
            comments = obj.comment_set.all()
            comment_form = CommentForm(request.POST or None)
            return render(request, 'video/video_detail.html', {
                'object':obj,
                'comments':comments,
                'comment_form':comment_form,
                })
    
        elif  obj.has_preview:
            return render(request, 'video/video_detail.html', {'object':obj,})

        else:
            # upgrade to become a member
            next_url = obj.get_absolute_url()
            return HttpResponseRedirect('%s?next=%s' % (reverse('upgrade'),next_url))
    

    else:
        next_url = obj.get_absolute_url()
        return HttpResponseRedirect('%s?next=%s' % (reverse('login'),next_url))


def category_list(request):
    queryset = Category.objects.all()
    return render(request, 'video/category_list.html', {'queryset':queryset,})

def category_detail(request, cat_slug):
    cat = get_object_or_404(Category,slug=cat_slug)
    page_view.send(
        sender = request.user,
        path = request.get_full_path(),
        primary_obj = cat,)
    return render(request, 'video/category_detail.html', {'object': cat,})

