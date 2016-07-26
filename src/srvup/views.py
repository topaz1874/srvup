# from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.forms import UserCreationForm, LoginForm
from analytics.signals import page_view
# @login_required(login_url='/enroll/login')
# @login_required
def home(request):

    page_view.send(
        sender=request.user,
        path=request.get_full_path())

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

