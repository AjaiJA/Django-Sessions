from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from .models import Employee
from django.contrib.sessions.models import Session

# Create your views here.

def home(request):
    if request.session.has_key('isLogged'):
        first_name=request.session.get('first_name')
        return render(request,"index.html",{'firstName':first_name})
    return redirect('/register/')

def register(request):
    if(request.method == "POST"):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        formData=Employee(first_name=first_name,last_name=last_name,email=email,password=password)
        try:
            formData.save()
            request.session["isLogged"]=True
            request.session['first_name']=first_name
            return redirect('/home/')
        except:
            pass
    elif request.session.has_key('isLogged'):
        first_name=request.session.get('first_name')
        return render(request,"index.html",{'firstName':first_name})
    return render(request,"register.html")

def login(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        if Employee.objects.filter(email=email, password=password).exists():
            isLog=Employee.objects.get(email=email, password=password)
            print(isLog.first_name)
            request.session["isLogged"]=True
            request.session['first_name']=isLog.first_name
            return redirect('/home/')
        else:
            msg='invalid Username or Password'
            return render(request,"register.html",{'err':msg})
    return redirect('/register/')

def logout(request):
    try:
        del request.session['isLogged']
        del request.session['first_name']
        return redirect('/register/')
    except KeyError:
        pass
    return render(request,"index.html")
