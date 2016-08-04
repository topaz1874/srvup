# from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from account.forms import UserCreationForm, LoginForm
from analytics.signals import page_view
from comment.models import Comment
from video.models import Video
# @login_required(login_url='/enroll/login')
# @login_required
"""
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from video.models import Video
from analytics.models import PageView
video_type = ContentType.objects.get_for_model(Video)

PageView.objects.filter(primary_content_type=video_type)\
.values("primary_object_id")\
.annotate(visit_count=Count("count"))\
.order_by("-visit_count")

PageView.objects.filter(primary_content_type=video_type)\
.values("primary_object_id")\
.annotate(most_pop_vid_count=Count("primary_object_id"))\
.order_by("-most_pop_vid_count")

"""

def home(request):
    if request.user.is_authenticated():
        page_view.send(
            sender=request.user,
            path=request.get_full_path())

        obj_lst = []
        # recent_comments = Comment.objects.get_recent(request.user)
        recent_videos = request.user.pageview_set.get_videos()
        recent_comments = request.user.comment_set.get_recent()
        video_type = ContentType.objects.get_for_model(Video)
        popular_videos_ids = request.user.pageview_set\
            .filter(primary_content_type=video_type)\
            .values_list("primary_object_id")\
            .annotate(the_count=Count("primary_object_id"))\
            .order_by('-the_count')
        popular_videos = []
        for i in popular_videos_ids:
            popular_videos.append(Video.objects.get(id=i[0]))

        for vid in recent_videos:
            obj =  vid.primary_content_object
            if obj not in obj_lst:
                obj_lst.append(obj) 


        context = {
        'obj_lst':obj_lst,
        'recent_comments': recent_comments,
        'popular_videos': popular_videos,
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

