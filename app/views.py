from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import ComputerConfig

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ComputerConfig  # Import your model

def home(request):
    if request.method == 'GET':
        # render the drawflow UI template
        return render(request, 'home.html')
    
    elif request.method == 'POST':

        data = request.POST.get('data')
        address = request.POST.get('address')
        config = ComputerConfig(config=data, address=address)
        config.save()

        if request.user.is_authenticated:
            sender = "jagadeeshgoudayr@gmail.com"
            subject = 'New computer order'
            message = f'You have received a new order for a computer with the following configuration: {data}. The delivery address is: {address}.'
            from_email = 'drawflow_app@example.com'
            send_mail(subject, message, from_email, [sender])
                
                # return a success response
            return HttpResponse('Your order has been placed successfully.')
        else:
            return HttpResponse("wrong email")
   
    


#register 

from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . forms import CreateUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
from .models import PreRegistration
from .forms import VerifyForm,LoginForm
from django.contrib.auth import login,logout,authenticate

def creatingOTP():
    otp = ""
    for i in range(6):
        otp+= f'{random.randint(0,9)}'
    return otp

def sendEmail(email):
    otp = creatingOTP()
    send_mail(
    'One Time Password',
    f'Your OTP pin is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )
    return otp


def createUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                otp = sendEmail(email)
                dt = PreRegistration(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username= form.cleaned_data['username'],email=email,otp=otp,password1 = form.cleaned_data['password1'],password2 = form.cleaned_data['password2'])
                dt.save()
                return HttpResponseRedirect('/verify/')
                
                
        else:
            form = CreateUser()
        return render(request,"newuser.html",{'form':form})
    else:
        return HttpResponseRedirect('/success/')


def verifyUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                data = PreRegistration.objects.filter(otp = otp)
                if data:
                    username = ''
                    first_name = ''
                    last_name = ''
                    email = ''
                    password1 = ''
                    for i in data:
                        print(i.username)
                        username = i.username
                        first_name = i.first_name
                        last_name = i.last_name
                        email = i.email
                        password1 = i.password1

                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    data.delete()
                    messages.success(request,'Account is created successfully!')
                    return HttpResponseRedirect('/home')   
                else:
                    messages.success(request,'Entered OTO is wrong')
                    return HttpResponseRedirect('/verify/')
        else:            
            form = VerifyForm()
        return render(request,'verify.html',{'form':form})
    else:
        return HttpResponseRedirect('/success/')

def success(request):
    if request.user.is_authenticated:
        return render(request,'success.html')
    else:
        return HttpResponseRedirect('/')

def logout_form(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
    
    
