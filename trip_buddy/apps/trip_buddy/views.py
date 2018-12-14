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
    return redirect ('/travels')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, 'Invalid Credentials', extra_tags = 'login')
        return redirect('/')
    user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['id'] = user.id
        return redirect ('/travels')
    else:
        messages.error(request, 'Invalid Password Credentials', extra_tags='login')
    return redirect('/')

def dashboard(request):
    if "id" not in request.session:
        return redirect('/')
    data = {
        'user': User.objects.get(id = request.session['id']),
        'my_trips':Trip.objects.filter(planned_by_id = request.session['id']).order_by('start'),
        'joined_trips':Trip.objects.filter(travelers = request.session['id']).order_by('start'),
        'other_trips':Trip.objects.exclude(planned_by_id = request.session['id']).exclude(travelers = request.session['id']).order_by('start')
    }
    return render(request, "dashboard.html", data)

def details(request, id):
    if "id" not in request.session:
        return redirect('/')
    data = {
        'trip': Trip.objects.get(id = id)
    }
    return render(request, 'details.html', data)

def addtrip(request):
    if "id" not in request.session:
        return redirect('/')
    return render(request, 'addtrip.html')

def newtrip(request):
    if "id" not in request.session:
        return redirect('/')
    start_date = None
    end_date = None
    error = False
    if len(request.POST) == 0 or len(request.POST['name']) == 0 or len(request.POST['description']) == 0 or len(request.POST['start']) == 0 or len(request.POST['end']) == 0:
        error = True
        messages.error(request,'Can not submit empty submission fields', extra_tags= 'newtrip')
    else:
        if request.POST['start'] !="":
            start_date = datetime.strptime(request.POST['start'], "%Y-%m-%d")
        if request.POST['end'] !="":
            end_date = datetime.strptime(request.POST['end'], "%Y-%m-%d")
        if start_date != None and end_date != None:
            if start_date < datetime.today():
                error = True
                messages.error(request, 'Initial Travel Date Can Not Predate Today', extra_tags = 'newtrip')
            if end_date < start_date:
                error = True
                messages.error(request, 'End Date Can Not Predate Initial Travel Date', extra_tags = 'newtrip')
    if error:
        return redirect('/addtrip')
    trip = Trip.objects.create(name = request.POST['name'], start = request.POST['start'], end = request.POST['end'], desc = request.POST['description'], planned_by_id = request.session['id'])
    return redirect('/travels') 

def join(request, id):
    if "id" not in request.session:
        return redirect('/')
    Trip.objects.get(id = id).travelers.add(request.session['id'])
    return redirect('/travels')

def cancel(request, id):
    if "id" not in request.session:
        return redirect('/')
    Trip.objects.get(id = id).travelers.remove(request.session['id'])
    return redirect('/travels')

def delete(request, id):
    if "id" not in request.session:
        return redirect('/')
    Trip.objects.get(id = id).delete()
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')