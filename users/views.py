import os
from django.conf import settings 
from .handler import handle_uploaded_file
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import PresonalDetailsForm,UserRegistrationForm,UserUpdateForm,ProfileUpdateForm,UserLoginForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PersonalDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
# Create your views here.
from .decorators import user_not_authenticated
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(uid,user)
    except:
        user = None
    print('in activate',user, account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you are logged in")
        login(request,user)
        return redirect('get_coord')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('get_coord')
'''
'''
def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("users/template_activate_account.html", 
        {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
@user_not_authenticated
def register(request):# have to add try block if user alredy exists!!!!!
    if request.method=='POST':
        k=list(request.POST.keys())
        v=list(request.POST.values())
        di=dict(zip(k[1:5],v[1:5]))
        user_form=UserRegistrationForm(di)
        print("new",user_form.is_valid())
        print(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            d2=dict()
            usn=user_form.cleaned_data.get('username')
            id=User.objects.get(username=usn).id
            print('id',type(id),id)
            d2['user']=str(id)
            d2.update(zip(k[5:],v[5:]))
            print(d2)
            detail_form=PresonalDetailsForm(d2)
            print("d2frm",detail_form.is_valid())
            if detail_form.is_valid():
                try:
                    detail_form.save()
                    activate_email(request,new_user,user_form.cleaned_data.get('email'))
                except Exception as err:
                    print(err)
                    new_user.delete()
                    for error in list(detail_form.errors.values()):
                        messages.error(request, error)
                else:
                    messages.success(request,'user acc created for {}'.format(usn))
                    new_user=User.objects.get(username=usn)
                    login(request,new_user)
                    return redirect('get_coord')
            else:
                new_user.delete()
        else:
            for error in list(user_form.errors.values()):
                messages.error(request, error)
            detail_form=PresonalDetailsForm()
            

    else:
        user_form=UserRegistrationForm()
        detail_form=PresonalDetailsForm()
    content={'user_form':user_form,'details':detail_form}
    return render(request,'users/register.html',content)
@login_required
def profile_pg(request):
    return render(request,'users/profile.html')
@user_not_authenticated
def custom_login(request):
    if request.method == 'POST':
        form=UserLoginForm(request=request,data=request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],
                          password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,f"Hello {user.username}")
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('get_coord')
                ''''''
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    form=UserLoginForm()
    return render(request,'users/login.html',{'form':form})
@login_required
def custom_logout(request):
    logout(request)
    #messages.info(request,'logged out sucessfully')
    return render(request,'users/logout.html')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,instance=request.user.personaldetails)
        print(request.POST,u_form.is_valid(), p_form.is_valid())
        print(request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'sucessesfully updated your profile')
            return redirect('users:profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.personaldetails)
    return render(request,'users/edit_profile.html',{'u_form':u_form,'p_form':p_form})

def send_user_email(request,form):
    subject='Request to place order made'
    message=render_to_string("users/email_to_user.html", 
        {'med_name':form.cleaned_data['medicine_name'],
         'user':request.user,
         'pharmacy_name':form.cleaned_data['pharma_name']
        })
    recipent_list=[request.user.email]
    email=EmailMessage(subject,message,to=recipent_list )
    email.send()
def send_email_with_attachment(request,path,form):
    subject='Request to order medicine'
    message=render_to_string("users/order_req.html", 
        {'med_name':form.cleaned_data['medicine_name'],
         'user':request.user,
         'quantity':form.cleaned_data['quantity'],
         'address':form.cleaned_data['delivery_address'],
         'phone_no':form.cleaned_data['phone_no'],
         'email':request.user.email,
        })
    recipent_list=[form.cleaned_data['pharma_email']]
    email = EmailMessage(subject,message,to=recipent_list )
    email.attach_file(f"{settings.BASE_DIR}/media/prescription/{path}")
    if email.send():
        pharma_name=form.cleaned_data['pharma_name']
        messages.success(request,f'Your request for order has been made to {pharma_name}')
    else:
        messages.error(request,'there was some error in placing the request for order')
    os.remove(f"{settings.BASE_DIR}/media/prescription/{path}")
@login_required
def request_order(request,**args):
    print(request.GET,args)
    user=request.user
    personal_detail=PersonalDetails.objects.get(user=user)
    address=personal_detail.address
    phone_no=personal_detail.phone_no
    value_={
    'pharma_name':args['pharma_name'],
    'medicine_name':args['med_name'],
    'quantity':0,
    'delivery_address':address,
    'phone_no':phone_no,
    'image':None,
    'pharma_email':args['pharma_email']}
    form=OrderForm(value_)
    print(form)
    print(form.is_valid())
    if request.method=='POST':
        form=OrderForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            path=handle_uploaded_file(request.FILES['image'])
            print(path,request.user.email)
            send_email_with_attachment(request,path,form)
            send_user_email(request,form)
        return redirect('get_coord')

    return render(request,'users/order_form.html',{'form':form})

# Create your views here.
