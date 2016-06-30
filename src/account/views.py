from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from .forms import UserCreationForm,LoginForm
from .models import MyUser
# Create your views here.
def user_register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        MyUser.objects.create_user(
            username=username,
            email=email,
            password=password
            )
        return redirect('login')
    context = {
        'form':form,
        'action':'',
        'btn':'Register',
    }
    return render(request, 'account/forms.html', context)

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if request.user.is_authenticated():
        messages.warning(request, 'You have already login.')
        return render(request, 'login.html',{'login_error':'haha' })

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'form':form,
                                                'login_error':'wrong password or username',})
    context = {
        'form': form,
    }
    return render(request, 'login.html' ,context)