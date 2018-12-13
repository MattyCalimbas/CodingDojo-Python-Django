from django.shortcuts  import render, HttpResponse, redirect
from django.contrib import messages
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
        messages.error(request,'Invalid Email Credentials', extra_tags= 'email')
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        error = True
        messages.error(request,'Invalid Email Credentials', extra_tags= 'email')
    if not EMAIL_REGEX.match(request.POST['email']): 
        error = True
        messages.error(request,'Invalid Email Credentials', extra_tags= 'email')
    if len(request.POST['first_name']) < 2 or len(request.POST['last_name']) < 2:
        error = True
        messages.error(request,'Invalid Credentials', extra_tags= 'name')
    if not NAME_REGEX.match(request.POST['first_name']):
        error = True
        messages.error(request,'Invalid Credentials', extra_tags= 'name')
    if not NAME_REGEX.match(request.POST['last_name']):
        error = True
        messages.error(request,'Invalid Credentials', extra_tags= 'name')
    if len(request.POST['password']) < 8:
        error = True
        messages.error(request,'Invalid Password Length', extra_tags= 'password')
    if request.POST['password'] != request.POST['confirm_pw']:
        error = True
        messages.error(request,'Invalid Password Submission', extra_tags= 'password')
    if error:
        return redirect('/')
    
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    decoded_hash = hashed.decode('utf-8')
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = decoded_hash )
    request.session['id'] = user.id
    return redirect ('/wall')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, 'Invalid Credentials', extra_tags = 'login')
        return redirect('/')
    user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['id'] = user.id
        return redirect ('/wall')
    else:
        messages.error(request, 'Invalid Credentials', extra_tags='login')
    return redirect('/')

def wall(request):
    if "id" not in request.session:
        return redirect('/')
    data = {
            'users': User.objects.all(),
            'user':User.objects.get(id = request.session['id'])
        }
    return render(request, 'wall.html', data)

def post_message(request):
    user = User.objects.get(id = request.session['id'])
    message = Message.objects.create(message = request.POST['message'], user_id = user)
    request.session['message'] = request.POST['message']
    return redirect('/wall')

def post_comment(request):
    user = User.objects.get(id = request.session['id'])
    comment = Comment.objects.create(comment = request.POST['comment'], message_id = Message.objects.get(id=request.POST['message_id']) , user_id = user)
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')
        