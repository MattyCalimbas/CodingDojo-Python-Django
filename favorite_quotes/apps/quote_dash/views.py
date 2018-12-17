from django.shortcuts  import render, HttpResponse, redirect
from django.contrib import messages
from time import strftime, localtime
from datetime import datetime
import re
import bcrypt
from . models import *

NAME_REGEX = re.compile(r'^[^0-9]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'index.html')

def registration(request):
    error = False
    if len(request.POST['email'])==0:
        error = True
        messages.error(request,'Invalid Email Length', extra_tags= 'email')
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        error = True
        messages.error(request,'Email Already Exits', extra_tags= 'email')
    if not EMAIL_REGEX.match(request.POST['email']): 
        error = True
        messages.error(request,'Invalid Email Credentials', extra_tags= 'email')
    if len(request.POST['first_name']) < 2 or len(request.POST['last_name']) < 2:
        error = True
        messages.error(request,'Invalid Name Submission', extra_tags= 'name')
    if not NAME_REGEX.match(request.POST['first_name']):
        error = True
        messages.error(request,'Invalid First Name Credentials', extra_tags= 'fname')
    if not NAME_REGEX.match(request.POST['last_name']):
        error = True
        messages.error(request,'Invalid Last Name Credentials', extra_tags= 'lname')
    if len(request.POST['password']) < 8:
        error = True
        messages.error(request,'Invalid Password Length', extra_tags= 'password')
    if request.POST['password'] != request.POST['confirm_pw']:
        error = True
        messages.error(request,'Confirmation Does Not Match Password Provided', extra_tags= 'cpassword')
    if error:
        return redirect('/')
    
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    decoded_hash = hashed.decode('utf-8')
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = decoded_hash )
    request.session['id'] = user.id
    return redirect ('/quotes')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, 'Invalid Credentials', extra_tags = 'login')
        return redirect('/')
    user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['id'] = user.id
        return redirect ('/quotes')
    else:
        messages.error(request, 'Invalid Password Credentials', extra_tags='login')
    return redirect('/')

def dashboard(request):
    if "id" not in request.session:
        return redirect('/')
    data = {
        'user': User.objects.get(id = request.session['id']),
        'quotes': Quote.objects.all()
    }
    return render(request, 'dashboard.html', data)

def post_quote(request):
    if "id" not in request.session:
        return redirect('/')
    error = False
    if len(request.POST['author']) < 3:
        error = True
        messages.error(request,'Invalid Author Submission Length', extra_tags= 'author')
    if len(request.POST['quote']) < 10:
        error = True 
        messages.error(request,'Invalid Quote Submission Length', extra_tags= 'quote')
    if error:
        return redirect('/quotes')
    quote = Quote.objects.create(author = request.POST['author'], quote= request.POST['quote'], posted_by_id = request.session['id'])
    return redirect ('/quotes')

def userdetails(request, id):
    if "id" not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id = id),
        'quotes': Quote.objects.filter(posted_by_id = id)
    }
    return render(request, 'userdetails.html', context)

def editaccount(request, id):
    if "id" not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id = id)
    }
    return render(request, 'editaccount.html', context)

def edituser(request):
    if "id" not in request.session:
        return redirect('/')
    error = False
    if len(request.POST['email'])==0:
        error = True
        messages.error(request,'Invalid Email Length', extra_tags= 'email')
    if not EMAIL_REGEX.match(request.POST['email']): 
        error = True
        messages.error(request,'Invalid Email Credentials', extra_tags= 'email')
    if len(request.POST['first_name']) < 2 or len(request.POST['last_name']) < 2:
        error = True
        messages.error(request,'Invalid Name Submission', extra_tags= 'name')
    if not NAME_REGEX.match(request.POST['first_name']):
        error = True
        messages.error(request,'Invalid First Name Credentials', extra_tags= 'fname')
    if not NAME_REGEX.match(request.POST['last_name']):
        error = True
        messages.error(request,'Invalid Last Name Credentials', extra_tags= 'lname')
    else:
        if request.POST['email'] !="":
            email = User.objects.get(id = request.session['id']).email  
            user_email = request.POST['email']
            if email == user_email:
                error = False
            else:
                error = True
                messages.error(request,'Email Already Exits', extra_tags= 'email')
    if error:
        return redirect('myaccount/'+str(request.session['id']))
    user = User.objects.get(id = request.session['id'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect ('myaccount/'+str(user.id))

def delete(request, id):
    if "id" not in request.session:
        return redirect('/')
    Quote.objects.get(id = id).delete()
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')
    


