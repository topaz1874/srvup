from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages

from video.models import Video
from notification.signals import notify
from .forms import CommentForm
from .models import Comment

# Create your views here.
def comment_thread(request, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm()

    return render(request, 'comment/comment_thread.html', {
        'form':form,
        'comment':comment,
        } )

def comment_create_view(request):
    if request.method == 'POST' and request.user.is_authenticated():
        video_id = request.POST.get('video_id')
        origin_path = request.POST.get('origin_path')
        parent_id = request.POST.get('parent_id')

        try:
            video = Video.objects.get(id=video_id)
        except:
            video = None

        try:
            parent = Comment.objects.get(id=parent_id)
        except:
            parent=None

        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']

            # create child comment
            if parent is not None and parent.video is not None:
                video = parent.video
                new_comment = Comment.objects.create_comment(
                    text=text,
                    video=video,
                    parent=parent,
                    author=request.user,
                    path=parent.get_origin)
                # print parent.get_origin # video url
                # print new_comment.get_origin #  video url 
                # print parent.get_absolute_url() parent  comment thread 
                # new_comment.get_absolute_url() new comment threads 

                # create a signal that parent comment user receive response
                notify.send(
                    sender=request.user, 
                    recipient=parent.author, 
                    verb='got an new response',
                    action=new_comment,
                    target=parent,
                    )

                messages.success(request, "Thanks for your response.")
                return HttpResponseRedirect(parent.get_absolute_url())

            # create parent comment 
            else:
                new_comment = Comment.objects.create_comment(
                    text=text,
                    video=video,
                    author=request.user,
                    path=origin_path)        
                # create a signal sending new comment add notification
                notify.send(
                    sender=request.user, 
                    recipient=new_comment.author, 
                    verb='posted new comment',
                    action=new_comment,
                    target=new_comment.video,
                    )                
                messages.success(request, "Thanks for your comment.")
                return HttpResponseRedirect(video.get_absolute_url())
        else:

            messages.warning(request, "Hey man you should enter somethin.")
            return HttpResponseRedirect(origin_path)

    else:
        return Http404