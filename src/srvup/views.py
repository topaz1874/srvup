# from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.forms import UserCreationForm, LoginForm
# @login_required(login_url='/enroll/login')
# @login_required
def home(request):
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

