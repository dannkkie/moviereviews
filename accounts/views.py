from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout 
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .forms import UserCreateForm

# Create your views here.
def signupaccount(request):
    context = {
        'form': UserCreateForm,
        'error': 'Passwords do not match',
    }
    if request.method == 'GET':
        return render(request, 'signupaccount.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form': UserCreateForm,'error': 'Username already taken. Choose new username.',})
        else:
            return render(request, 'signupaccount.html', context)

@login_required        
def logoutaccount(request):
    logout(request)
    return redirect('home')

def loginaccount(request):    
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  
        if user is None:
            return render(request,'loginaccount.html',{'form': AuthenticationForm,'error': 'username and password donot match'})
        else:
            login(request,user)
            return redirect('home')