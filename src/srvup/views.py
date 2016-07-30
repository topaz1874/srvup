# from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.forms import UserCreationForm, LoginForm
from analytics.signals import page_view
from comment.models import Comment
# @login_required(login_url='/enroll/login')
# @login_required
def home(request):
    if request.user.is_authenticated():
        page_view.send(
            sender=request.user,
            path=request.get_full_path())

        obj_lst = []
        # recent_comments = Comment.objects.get_recent(request.user)
        recent_videos = request.user.pageview_set.get_videos()
        recent_comments = request.user.comment_set.get_recent()
        for vid in recent_videos:
            obj =  vid.primary_content_object
            if obj not in obj_lst:
                obj_lst.append(obj) 
        context = {
        'obj_lst':obj_lst,
        'recent_comments': recent_comments,
        }
        return render(request, 'home_logged_in.html',context)
    else:
        register_form = UserCreationForm()
        login_form = LoginForm()
        context = {
        'register_form': register_form,
        'login_form': login_form,
        }
        return render(request, "home.html", context)

@login_required(login_url='/login/')
def staff_home(request):
    return render(request, 'home.html', context={})

