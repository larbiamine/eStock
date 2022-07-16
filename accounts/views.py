from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
            if(User.objects.filter(username=username).exists()):
                print('nom d utilisateur exist deja')
                messages.info(request,'nom d utilisateur exist deja')
            elif User.objects.filter(email=email).exists(): 
                print('email taken')
                messages.info(request,'email taken')
            else:    
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')   
        else:
            print('les mots de passe ne correspondent pas')
            messages.info(request,'les mots de passe ne correspondent pas')
        return redirect('register')
    else:
        return render(request,'register.html')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print('user logged in')
            return redirect('/dashboard')
        else:
            messages.info(request,'user doesnt exist')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')