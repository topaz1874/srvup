from django.shortcuts import render, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Video,Category
from comment.models import Comment
from comment.forms import CommentForm

@login_required
def video_detail(request,cat_slug,vid_slug):
    try:
        cat = Category.objects.get(slug=cat_slug)
    except:
        return Http404
    try:
        obj = Video.objects.get(slug=vid_slug, category=cat)
        comments = obj.comment_set.all()
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            Comment.objects.create_comment(
                text=text,
                video=obj,
                author=request.user,
                path=request.get_full_path())
            return HttpResponseRedirect(obj.get_absolute_url())

        return render(request, 'video/video_detail.html', {
            'object':obj,
            'comments':comments,
            'comment_form':comment_form,})
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
