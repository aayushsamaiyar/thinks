from django import http
from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request,'home/home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
            messages.error(request,'please fill the form correctly.')
        
        else:
            contact = Contact(name = name, email = email, phone = phone, content = message)
            contact.save()
            messages.success(request,'your message has been registered.')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        querypost = Post.objects.none()
    else:
        querypostTitle = Post.objects.filter(title__icontains = query)
        querypostAuthor = Post.objects.filter(author__icontains = query)
        querypostContent = Post.objects.filter(content__icontains = query)
        querypost = querypostTitle.union(querypostAuthor,querypostContent)
    
    if querypost.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    
    params = {'querypost': querypost, 'query':query}
    return render(request, 'home/search.html', params)


# authentication APIS

def handleSignup(request):
    if request.method == 'POST':
       #get post parameters
       username = request.POST['username'] 
       fname = request.POST['fname'] 
       lname = request.POST['lname'] 
       email= request.POST['email'] 
       pass1 = request.POST['pass1'] 
       pass2 = request.POST['pass2'] 

       if len(username) > 30:
           messages.error(request,'username must be under 30 characters')
           return redirect('home')
        
       if not username.isalnum():
           messages.error(request,'username should contain letter and numbers.')
           return redirect('home')
      
       if (pass1 != pass2):
           messages.error(request, "passwords do not match")
           return redirect('/')

         

       myuser = User.objects.create_user(username, email, pass1)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.save()
       messages.success(request, " your account has been successfully created.")
       return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
       loginusername = request.POST['loginusername'] 
       loginpassword = request.POST['loginpass'] 

       user = authenticate(username = loginusername, password = loginpassword)
       if user is not None:
           login(request, user)
           messages.success(request, "successfully logged in")
           return redirect('home')
       else:
           messages.error(request, "invalid user credentials. Please try again.")
           return redirect('home')
    return HttpResponse("")

def handleLogout(request):
    logout(request)
    messages.success(request,"successfully logged out.")
    return redirect('home')