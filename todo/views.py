from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import TodoForm
from django.contrib.auth import login


def home(request):
    return render(request,'todo/home.html')


def signupuser(request):
    if request.method =='GET':
        return render(request,'todo/singupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/singupuser.html',{'form': UserCreationForm(), 'error': 'Это имя пользователя уже используется'})
        else:
            return render(request, 'todo/singupuser.html', {'form': UserCreationForm(),'error':'Password did not match(пароль не совпадает)'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error':'имя пользователя и пароль не совпадают'})
        else:
            login(request, user)
            return redirect('currenttodos')
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error':'Переданы не верные данные'})
def currenttodos(request):
    return render(request, 'todo/currenttodos.html')