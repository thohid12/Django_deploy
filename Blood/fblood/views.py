from django.shortcuts import render,redirect,HttpResponse

from  .models import Donar_signup_info,signup_info,Donar_donate_info,FindInfo,PreviousInfo,ProfileInfo
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils.dateparse import parse_date

from django.db.models import F

from django.utils.timezone import localdate
from django.contrib import  messages
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout





# Create your views here.
def signup(request):
    if request.method == "POST":
        phone=request.POST["phone"]
        password=request.POST["password"]
        c_password=request.POST["c_password"]
        email=request.POST["email"]
        exists_phone = User.objects.filter(username=phone).exists()
        exists_mail= User.objects.filter(email=email).exists()
       
        if(password==c_password and len(phone)==11 and exists_phone==False and exists_mail==False):
            info = User.objects.create_user(username=phone,password=password,email=email)
            info.save()
            return redirect('Login')
        else:
            messages.error(request,"Password and confirm password doesn't match or this phone number or email are already registered or wrong")
            return redirect('signup')
    else:
        return render(request,'signup.html')
    
    
def Login(request):
    if request.method == "POST":
        val=1
        phone=request.POST["phone"]
        password=request.POST["password"]
        #phone1=phone
        #exists = Donar_signup_info.objects.filter(phone=phone,password=password).exists()
       #exists=authenticate(request,username=phone,password=password)
        user = authenticate(request, username=phone, password=password)
        print(user)
        #exists = User.objects.filter(phone=phone,password=password).exists()
       
        if user is not None:
            login(request,user)
            #return render(request,'home.html',{"phone":phone,"val":val})
            return redirect(f'{reverse("home")}?phone={phone}')

        else:
            messages.error(request,"Wrong phone number or password")
            return redirect('Login')
    else:
        return render(request,'login.html') 

@login_required(login_url='Login')
def home(request):
    val=0
    phone = request.GET.get('phone')
    if phone:
        val=1
        return render(request,'home.html',{"phone":phone,"val":val})
    else:
        return render(request,'home.html',{"val":val})
        
        

@login_required(login_url='Login')
def donate(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("image")  # Assuming the input field name is "file"
        name=request.POST["fullName"]
        phone=request.POST["phone"]
        blood=request.POST["BloodGroup"]
        """ print(phone) """
        """ blood=blood.upper() """
        print(blood)
        date=request.POST["lastDate"]
        district=request.POST["district"]
        police=request.POST["policeStation"]
        exists = User.objects.filter(username=phone).exists()
        exists1 = Donar_donate_info.objects.filter(phone=phone).exists()
        print(exists)
        print(exists1)
        
        if uploaded_file:
            # Process the uploaded image (e.g., save it to a model)
            print("upload")
            if(len(phone)!=11 or exists!=True or exists1==True):
                messages.error(request,"You have submitted wrong information or this phone number already donate")
                print("unsave")
                return redirect('donate')
            
            
            else:
                info = Donar_donate_info(name=name,phone=phone,blood=blood,date=date,district=district,police=police,img=uploaded_file)
                info.save()
                print("save")
                messages.success(request,"All information have been submitted successfully")
                return redirect('donate')
               #return render(request, "body.html") 
            
            
               #image_instance = Donar_info(img=uploaded_file)
               #image_instance.save()
               #return HttpResponse("Image uploaded successfully!")

    else:
         print("meo")
         return render(request,'donate.html')

@login_required(login_url='Login')      
def find(request):
    if request.method == "POST":
        blood=request.POST["BloodGroup"]
        date=request.POST["blood_requre_date"]
        district=request.POST["district"]
        police=request.POST["policeStation"]
        count=0
        temp = []
        fetch=Donar_donate_info.objects.all()
        
        for info in fetch:
            #tot=(date-info.last).days
            date1 = parse_date(date)
            date2 = parse_date(info.date)
            difference= date1 - date2
            days = difference.days
            print(difference)
            print(days)
            if(info.blood == blood and days>=121 and info.district == district and info.police == police):
                count+=1
                address= info.police + ", " + info.district
                obj=FindInfo()
                obj.name=info.name
                obj.phone=info.phone
                obj.blood=info.blood
                obj.address=address
                obj.img=info.img
                """ temp=FindInfo(name=info.name,phon=info.phone,blood=info.blood,address=address,img=info.img) """
                temp.append(obj)
                """ temp.save() """
        if(count==0):
                messages.error(request,"Sorry! There aren't any donors available in your criteria.")
                return redirect('find')
        else:
            print("2")
            messages.success(request,"Sorry! There aren't any donors available in your criteria.")
            return render(request,'find.html',{"fabs":temp})
        
    else:
        return render(request,'find.html')
    
    
@login_required(login_url='Login')
def profile(request):
   if request.method == "POST":
        phone=request.POST["phoneNumber"]
        print(phone)
        Total=0
        fetch=PreviousInfo.objects.all()
        for info in fetch:
            if(phone==info.phone):
                Total+=1
        
        count=0
        temp = []
        fetch=Donar_donate_info.objects.all()
        for info in fetch:
            if(phone==info.phone):
                count+=1
                address= info.police + ", " + info.district
                obj=ProfileInfo()
                obj.name=info.name
                obj.phone=info.phone
                obj.blood=info.blood
                obj.address=address
                obj.img=info.img
                today = datetime.today().date()
                date_string = str(today)  # Convert date to string
                date1 = parse_date(date_string)
                date2 = parse_date(info.date)
                difference= date1 - date2
                days = difference.days
                DaysLeft=121-days
                datetime_object = datetime.strptime(date_string,'%Y-%m-%d')
                new_date = datetime_object + timedelta(days=DaysLeft)
                new_date_str = new_date.strftime("%Y-%m-%d")
                obj.LastDate=info.date
                obj.DaysLeft=DaysLeft
                obj.TotalDonate=Total+1
                obj.ProbableDate=new_date_str
                temp.append(obj)
                return render(request,'profile.html',{"fabs":temp,"val":count})
        if(count == 0):
            return render(request,'profile.html',{"val":count,"phone":phone})
        
                
@login_required(login_url='Login')       
def update(request):
    if request.method == "POST":
        updated_file = request.FILES.get("image")  # Assuming the input field name is "file"
        updated_phone=request.POST["phone"]
        updated_mail=request.POST["updated_email"]
        
        if(Donar_donate_info.objects.filter(phone=updated_phone).exists()==True or 
           User.objects.filter(username=updated_phone).exists()==True or 
           PreviousInfo.objects.filter(phone=updated_phone).exists()==True or
           User.objects.filter(email=updated_mail).exists()==True ):
                messages.error(request,"Your updated phone or email already exist in other account")
                return redirect('update')
        
        
        
        
        
        updated_date=request.POST["lastDate"]
        updated_district=request.POST["district"]
        updated_police=request.POST["policeStation"]
        previous_phone=request.POST["HiddenPhone"]
        exists = Donar_donate_info.objects.filter(phone=previous_phone).exists()
        if(exists==True):
            updated_info = Donar_donate_info.objects.get(phone=previous_phone)
            if updated_file:
                os.remove(updated_info.img.path)
                updated_info.img=updated_file
            if(len(updated_phone)>0):
                updated_phone_signup=User.objects.get(username=previous_phone)
                updated_phone_signup.username=updated_phone
                updated_phone_signup.save()
                update_previousinfo=PreviousInfo.objects.all()
                for info in update_previousinfo:
                    if(previous_phone==info.phone):
                        PreviousInfo.objects.filter(phone=previous_phone).update(phone=updated_phone)
                
                updated_info.phone=updated_phone
                
            if(len(updated_date)>0):
                previous=PreviousInfo(phone=updated_info.phone,date=updated_info.date)
                previous.save()
                updated_info.date=updated_date
            if(len(updated_district)>0):
                updated_info.district=updated_district
            if(len(updated_police)>0):
                updated_info.police=updated_police
            updated_info.save()
        
        else:
            if(len(updated_phone)>0):
                updated_phone_signup=User.objects.get(username=previous_phone)
                updated_phone_signup.username=updated_phone
                
            if(len(updated_mail)>0):
                updated_phone_signup=User.objects.get(username=previous_phone)
                updated_phone_signup.email=updated_mail
            updated_phone_signup.save()  
                
        #sending messages based on email and phone 
        if(len(updated_phone)>0 and len(updated_mail)>0):
            messages.success(request,"Your phone or email are updated")
            return render(request,'update.html',{"phone":updated_phone,"val":1})
        elif(len(updated_phone)>0 and len(updated_mail)==0):
            messages.success(request,"Your phone is updated")
            print(updated_phone)
            return render(request,'update.html',{"phone":updated_phone,"val":1})
        elif(len(updated_phone)==0 and len(updated_mail)>0):
            messages.success(request,"Your email is updated")
            return render(request,'update.html',{"phone":previous_phone})
        else:
            return render(request,'update.html',{"phone":previous_phone})
        
            
            
            
    else:      
        return render(request,'update.html')
    
    
def Logout(request):
    logout(request)
    return redirect('Login')