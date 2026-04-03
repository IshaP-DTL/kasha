from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import re
from .tokens import *
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
import random
from django.conf import settings
from google import genai
import json
from django.db.models import Q
from .delivery_tokens import generateDeliveryToken,verifyDeliveryToken
from django.db import transaction
import datetime
from textblob import TextBlob



# Create your views here.
def homePage(request):
    return render(request, "home-03.html")
# def homeThree(request):
#     return render(request, "home-03.html")
def about(request):
    return render(request, "about.html")
def blog(request):
    return render(request, "blog.html")
def blogDetail(request):
    return render(request, "blog-detail.html")
def contact(request):
    return render(request, "contact.html")
def Product(request):
    return render(request, "product.html")
def productDetail(request):
    return render(request, "product-detail.html")
def shopingCart(request):
    return render(request, "shoping-cart.html")
def checkout(request):
    return render(request, "checkout.html")
def login_view(request):
    return render(request, "login.html")
def register_view(request):
    return render(request, "register.html")
def profile_view(request):
    return render(request,"profile.html")
def logout_view(request):
    logout(request)
    return redirect('login')
def forgetpassword(request):
    return render(request,"forgetpassword.html")
def verifyotppage(request):
    return render(request,"verifyotp.html")
def resetpassword(request):
    return render(request,"resetpassword.html")
def wishlistpage(request):
    return render(request,"wishlistpage.html")
def delivery_login(request):
    return render(request,"delivery_login.html")
def delivery_dashboard(request):
    return render(request,"delivery_dashboard.html")
def orderpage(request):
    return render(request,"orderpage.html")
def acceptPage(request, order_id):
    try:
        orderObj = order.objects.get(order_id=order_id)

        items = orderItems.objects.filter(order_id=orderObj)

        itemList = []
        for i in items:
            itemList.append({
                "product": i.product_id.product_name,
                "quantity": i.quantity,
                "size": i.size.size_name
            })

        context = {
            "order": orderObj,
            "items": itemList
        }

        return render(request, "accept.html", context)

    except order.DoesNotExist:
        return JsonResponse({"message": "Order not found"})
def delivery_order_details(request):
    return render(request,"delivery_order_details.html") 
def orderDetailsPage(request):
    return render(request,"orderdetails.html")
 



 
# DATE FUNCTION:
 
def format_date(date_value):
    if not date_value:
        return None
 
    try:
        return datetime.datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
   
# COUNTRY API
@csrf_exempt
@api_view(['POST'])
def countryDetail(request):
    try:
        countryName=request.data.get('countryName')
        if not countryName:
            return JsonResponse({'status':False,'message':'country name is required.'},status=400)
        countryCode=request.data.get('countryCode')
        if not countryCode:
            return JsonResponse({'status':False,'message':'country code is required.'},status=400)
        dialCode=request.data.get('dialCode')
        if not dialCode:
            return JsonResponse({'status':False,'message':'dialcode  is required.'},status=400)
        if user.objects.filter(country_name=countryName).exists():
            return JsonResponse({"message": "Email already registered"}, status=400)
        country.objects.create(
            country_name=countryName,
            country_code=countryCode,
            dial_code=dialCode
        )
        return JsonResponse({'status': True, 'message': 'Success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':False,'message':'str(e)'},status=500)
    
#GETALLCOUNTRY API
@csrf_exempt
@api_view(["GET"])
def getAllCountry(request):
    try:
        countries = country.objects.all()

        data = []
        for co in countries:
            data.append({
                "countryId": co.country_id,
                "countryName": co.country_name,
                "countryCode": co.country_code,
                "dialCode": co.dial_code
            })

        return JsonResponse({"data": data}, status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status = 500)   

#GETCOUNTRYBY-ID API
@csrf_exempt   
@api_view(["GET"])
def getCountryById(request):
    try:
        countryId = request.GET.get("countryId")
        if not countryId:
            return JsonResponse({"message":"pls send country ID!!"},status=400)
        try:
            countryObj = country.objects.get(country_id=countryId)
        except country.DoesNotExist:
            return JsonResponse({"message":"country not found!!"},status=404)
        data={
            "country_id":countryObj.country_id,
            "country_name":countryObj.country_name,
            "country_code":countryObj.country_code,
            "dial_code":countryObj.dial_code
        }
        return JsonResponse({"data": data}, status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)
    
#STATE API
@csrf_exempt
@api_view(["POST"]) 
def CreateState(request):
    try:
        stateName=request.data.get("stateName")
        countryId=request.data.get("countryId")
        if not stateName or len(stateName)<=2:
            return JsonResponse({"message":"enter valid length name!!!"},status=400)
        if user.objects.filter(state_name=stateName).exists():
            return JsonResponse({"message": "statename already registered"}, status=400)
        try:
            countryObj=country.objects.get(country_id=countryId)
        except country.DoesNotExist:
            return JsonResponse({"message":"country not found!!!"},status=404)
        state.objects.create(
            state_name=stateName,
            country_id=countryObj
        )
        return JsonResponse({"message":"state created"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)

#GET ALLSTATE API
@csrf_exempt 
@api_view(["GET"])
def getAllState(request):
    try:
        states = state.objects.all()

        data = []
        for st in states :
            data.append({
                "countryId": st.country_id.country_id,
                "stateName": st.state_name,
                "stateId": st.state_id,
            })


        return JsonResponse ({"data":data},status = 200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status = 500)
    
#STATEBY ID -API
@csrf_exempt
@api_view(["GET"])
def getStateById(request):
    try:
        stateId = request.GET.get("stateId")
        if not stateId:
            return JsonResponse({"message":"pls send State ID!!"},status=400)
        try:
            stateObj = state.objects.get(state_id=stateId)
        except state.DoesNotExist:
            return JsonResponse({"message":"state not found!!"},status=404)
        stateObj={
            "id":stateObj.state_id,
            "name":stateObj.state_name,
            "country_Id":stateObj.country_id.country_name
        }
        return JsonResponse({"data":stateObj},status = 200)
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)   
        
#CITY API
@csrf_exempt
@api_view(['POST'])
def CreateCity(request):
    try:
        cityName=request.data.get("cityName")
        stateId=request.data.get("stateId")
        if not cityName or len(cityName) <=2:
            return JsonResponse({"message":"enter vaild legth name!!"},status=400)
        if user.objects.filter(city_name=cityName).exists():
            return JsonResponse({"message": "city already registered"}, status=400)
        try:
            stateObj=state.objects.get(state_id=stateId)
        except state.DoesNotExist:
            return JsonResponse({"message":"state not found!!"},status=404)
        city.objects.create(
            city_name=cityName,
            state_id=stateObj
        )
        return JsonResponse({"message":"city created"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
    
# 11) GET ALL CITY 
@csrf_exempt
@api_view(["GET"])
def getAllCity(request):
    try:
        cities = city.objects.all()

        data = []
        for ct in cities:
            data.append({
                "cityId": ct.city_id,
                "cityName": ct.city_name,
                "stateId": ct.state_id.state_id
            })

        return JsonResponse({"data": data}, status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status = 500)  

# 12) GET CITY BY ID
@csrf_exempt
@api_view(["GET"])
def getcityById(request):
    try:
        cityId = request.GET.get("cityId")
        if not cityId:
            return JsonResponse({"message":"pls send city ID!!"},status=400)
        try:
            cityObj = city.objects.get(city_id=cityId)
        except city.DoesNotExist:
            return JsonResponse({"message":"city not found!!"},status=404)
        cityObj={
            "id":cityObj.city_id,
            "name":cityObj.city_name,
            "stateId":cityObj.state_id.state_name
        }
        return JsonResponse({"data":cityObj},status = 200)
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)
   
#PINCODE API
@csrf_exempt
@api_view(['POST'])
def CreatePincode(request):
    try:
        Pincode = request.data.get("Pincode")
        cityId = request.data.get("cityId")
        if not Pincode or len(Pincode)>6:
            return JsonResponse({"message":"enter valid pincode!!"},status=400)
        try:
            cityObj = city.objects.get(city_id=cityId)
        except city.DoesNotExist:
            return JsonResponse({"message":"city not found!!"},status=404)
        pincode.objects.create(
            Pincode = Pincode,
            city_id=cityObj
        )
        return JsonResponse({"message":"pincode created"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)

# GET PINCODE BY PINCODE   
@csrf_exempt
@api_view(["GET"])
def getPincodeByPincode(request):
    try:
        Pincode = request.GET.get("Pincode")
        if not pincode:
            return JsonResponse({"message":"pls send pincode!!"},status=400)
        try:
            pincodeObj = pincode.objects.get(Pincode=Pincode)
        except pincode.DoesNotExist:
            return JsonResponse({"message":"pincode not found!!"},status=404)
        pincodeObj={
            "id":pincodeObj.pincode_id,
            "pincode":pincodeObj.Pincode,
            "cityId":pincodeObj.city_id.city_id
        }
        return JsonResponse({"data":pincodeObj},status = 200)
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)
    
#USER API
@csrf_exempt
@api_view(['POST'])
def CreateUser(request):
    try:
        userName=request.data.get("userName")
        countryCode=request.data.get("countryCode")
        phoneNo=request.data.get("phoneNo")
        Email=request.data.get("Email")
        passWord=request.data.get("passWord")
        confirmPassword=request.data.get("confirmPassword")
        if not userName:
            return JsonResponse({"error":"username is required"},status=400)
        if not userName or len(userName) <=2:
            return JsonResponse({"error":"username must be longer than 2 char!!"},status=400)
        if not countryCode:
            return JsonResponse({"error":"dialcode is required"},status=400)
        if not phoneNo:
            return JsonResponse({"error":"phoneNumber is required"},status=400)
        if not phoneNo.isdigit():
            return JsonResponse({"error":"phoneNum must be in digit"},status=400)
        if not Email:
            return JsonResponse({"error":"Email is required"},status=400)
        Email=Email.strip().lower()
        EmailRegex= r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(EmailRegex,Email):
            return JsonResponse({"error":"invalid format"},status=400)
        if not passWord or len(passWord) <8:
            return JsonResponse({"error":"passWord must be 8 char"},status=400)
        if not confirmPassword:
            return JsonResponse({"error":"confirmPassword is required"},status=400)
        if passWord!=confirmPassword:
            return JsonResponse({"error":"password and confirm password do not match"},status=400)
        if user.objects.filter(email=Email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)
        if user.objects.filter(phone_number=phoneNo).exists():
            return JsonResponse({"error": "Phone number already registered"}, status=400)
        try:
            countryObj=country.objects.get(country_code=countryCode)
        except country.DoesNotExist:
            return JsonResponse({"error":"country not found"},status=404)
        hashed_password = make_password(passWord)
        user.objects.create(
          username=userName,
          country_code=countryObj,
          phone_number=phoneNo,
          email=Email,
          password=hashed_password
        )
        return JsonResponse({"message":"user created!!!"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
    
#LOGIN API  
@csrf_exempt
@api_view(['POST'])
def LoginUser(request):
    try:
        Email = request.data.get("Email")
        passWord = request.data.get("passWord")

        if not Email:
            return JsonResponse({"error": "Email is required"}, status=400)

        Email = Email.strip().lower()
        EmailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(EmailRegex, Email):
            return JsonResponse({"error": "invalid email format"}, status=400)

        if not passWord:
            return JsonResponse({"error": "Password is required"}, status=400)

        try:
            userObj = user.objects.get(email=Email)
        except user.DoesNotExist:
            return JsonResponse({"error": "user not found"}, status=404)

        if not check_password(passWord, userObj.password):
            return JsonResponse({"error": "password not matched"}, status=401)

        token = generateToken(userObj.user_id)

        return JsonResponse({
            "message": "login successfully",
            "userName": userObj.username,
            "email": userObj.email,
            "token": token
        }, status=200)

    except Exception as e:
        print("LOGIN ERROR:", e)  
        return JsonResponse({"error": str(e)}, status=500)
#verify user API  
@csrf_exempt
@api_view(["GET"])
def verify_user_token(request):
 
    token = request.headers.get("token")
 
    if not token:
        return JsonResponse({"valid": False}, status=401)
 
    try:
 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
 
        user_id = payload.get("user_id")
 
        return JsonResponse({
            "valid": True,
            "user_id": user_id
        })
 
    except jwt.ExpiredSignatureError:
        return JsonResponse({"valid": False, "message": "Token expired"}, status=401)
 
    except jwt.InvalidTokenError:
        return JsonResponse({"valid": False, "message": "Invalid token"}, status=401)
 

# FORGOT PASSWORD:
@csrf_exempt
@api_view(["POST"])
def forgotPassword(request):
    try:
        email = request.data.get("email")
 
        if not email:
            return JsonResponse({"Message": "Email is required"}, status=400)
 
        userObj = user.objects.filter(email=email).first()
        if not userObj:
            return JsonResponse({"Message": "User not found"}, status=404)
 
        # Generate OTP
        generatedOtp = random.randint(100000, 999999)
        print(generatedOtp)
 
        send_mail(
            subject="Forgot Password OTP",
            message=f"Your OTP is {generatedOtp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        userObj.otp = generatedOtp
        userObj.save()
        return JsonResponse(
            {"Message": "OTP sent to email"},
            status=200
        )
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
# verify OTP:
@csrf_exempt
@api_view(["POST"])
def verifyOtp(request):
    try:
        email = request.data.get("email")
        print(email)
        otp = int(request.data.get("otp"))
        print(otp)
        if not email or not otp:
            return JsonResponse({"Message": "Email and OTP are required"},status=400)
 
        userObj = user.objects.filter(email=email).first()
        if not userObj:
            return JsonResponse({"Message": "User not found"}, status=404)
 
        if userObj.otp != otp:
            return JsonResponse({"Message": "Invalid OTP"}, status=400)
        print(userObj)
        userId = userObj.user_id
        token = generateToken(userId)
        print(token)
        return JsonResponse(
            {
                "Message": "OTP verified successfully",
                "token": token
            },
            status=200
        )
 
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=500)
 
# set Passward    
@csrf_exempt
@api_view(["POST"])
def setNewPassword(request):
    try:
        email = request.data.get("email")
        otp = request.data.get("otp")
        newPassword = request.data.get("newPassword")
        confirmPassword = request.data.get("confirmPassword")

        if not email:
            return JsonResponse({"message":"This field is required"}, status=400)

        if newPassword != confirmPassword:
            return JsonResponse({"message":"Passwords do not match"}, status=400)

        userObj = user.objects.filter(email=email).first()
        if not userObj:
            return JsonResponse({"message":"User not found"}, status=404)

        userObj.password = make_password(newPassword)
        userObj.otp = None
        userObj.save()

        return JsonResponse({"message":"Password reset successful"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# 19) RESET PASSWORD
@csrf_exempt
@api_view(["PUT"])
def resetPassword(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"Message":"Please login first!!"}, status=400)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"Message":"User not found!!"}, status=404)

        oldPassword = request.data.get("oldPassword")
        newPassword = request.data.get("newPassword")
        confirmPassword = request.data.get("confirmPassword")

        if not oldPassword or not newPassword:
            return JsonResponse({"Message":"Old password and new password are required"},status=400)
        if newPassword != confirmPassword:
            return JsonResponse({"error":"new password and confirm passward are not same!!"}, status=400)
        if not check_password(oldPassword, userObj.password):
            return JsonResponse({"Message":"Old password is incorrect"},status=400)

        userObj.password = make_password(newPassword)
        userObj.save()

        return JsonResponse({"Message":"Password updated successfully"},status=200)

    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)

# 13)USER PROFILE API
@csrf_exempt
@api_view(["POST"])
def createUserProfile(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error":"Please login first!!"}, status=400)        
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()

        activeProfile = profile.objects.filter(
            user_id=userObj,
            is_deleted=False,
            is_active=True
        ).first()

        if activeProfile:
            return JsonResponse(
                {"error": "Profile already exists"},
                status=400
            )
 
        firstName = request.data.get("firstName")
        lastName = request.data.get("lastName")
        gender = request.data.get("gender")
        dateOfBirth = format_date(request.data.get("dateOfBirth"))
        profilePicture = request.data.get("profilePicture")
 
        if not firstName:
            return JsonResponse({"error":"please enter fisrtname!!"},status=400)
        if not lastName:
            return JsonResponse({"error":"please enter lastname!!"},status=400)
        if gender is None:
            return JsonResponse({"error":"please enter gender"},status=400)
       
        dateOfBirth = format_date(request.data.get("dateOfBirth"))
 
        if not dateOfBirth:
            return JsonResponse({"error": "please enter birthdate"}, status=400)
   
        profile.objects.create(
            user_id=userObj,
            first_name=firstName,
            last_name=lastName,
            gender=gender,
            DOB=dateOfBirth,
            profile_picture=profilePicture,
            is_active=True,
            is_deleted=False
        )
        return JsonResponse({"message":"profile created"},status=200)
   
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)
    
# GET USER PROFILE
@csrf_exempt
@api_view(["GET"])
def getUserProfile(request):
 
    token = request.headers.get("token")
    if not token:
        return JsonResponse({"error": "Login required"}, status=401)
    userIdOrError = verifyToken(token)
 
    if isinstance(userIdOrError, dict):
        return JsonResponse(userIdOrError, status=401)
 
    try:
        userObj = user.objects.get(user_id=userIdOrError)
    except user.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    try:
        profileObj = profile.objects.filter(user_id=userObj,is_deleted=False,is_active=True).first()
    except profile.DoesNotExist:
        return JsonResponse({"error":"Profile not found!!"}, status=404)
    if not profileObj:
        return JsonResponse({"profile": None}, status=200)
 
    profile_pic_url = ""
    if profileObj.profile_picture:
        profile_pic_url = profileObj.profile_picture.url
 
    return JsonResponse({

        "user": {
            "email": userObj.email,
            "phone": userObj.phone_number
        },

        "profile": {
            "profile_id": profileObj.profile_id,
            "first_name": profileObj.first_name,
            "last_name": profileObj.last_name,
            "gender": profileObj.gender,
            "DOB": profileObj.DOB.strftime("%Y-%m-%d"),
            "profile_picture": profile_pic_url
        }

    }, status=200)

# 14) UPDATE USER PROFILE
@csrf_exempt
@api_view(["PUT"])
def updateUserProfile(request):
   try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Login required"}, status=401)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        # profile_id = request.data.get("profile_id")
        # if not profile_id:
        #     return JsonResponse({"error": "profile_id required"}, status=400)
 
        try:
            profileObj = profile.objects.get(
                user_id=userIdOrError,
                is_deleted=False,
                is_active=True
            )
        except profile.DoesNotExist:
            return JsonResponse({"error": "Profile not found"}, status=404)
 
        # UPDATE FIELDS
        if request.data.get("firstName"):
            profileObj.first_name = request.data.get("firstName")
 
        if request.data.get("lastName"):
            profileObj.last_name = request.data.get("lastName")
 
        if request.data.get("gender"):
            profileObj.gender = request.data.get("gender")
 
        if request.data.get("dateOfBirth"):
            profileObj.DOB = format_date(request.data.get("dateOfBirth"))
 
        if request.data.get("profilePicture"):
            profileObj.profile_picture = request.data.get("profilePicture")
 
        profileObj.save()
 
        return JsonResponse({"message": "Profile updated"}, status=200) 
   except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
  
# 15)DELETE USER PROFILE
@csrf_exempt
@api_view(["DELETE"])
def deleteUserProfile(request):
    token = request.headers.get("token")
    if not token:
        return JsonResponse({"Message": "Login required"}, status=400)

    userIdOrError = verifyToken(token)
    if isinstance(userIdOrError, dict):
        return JsonResponse(userIdOrError, status=401)

    userObj = user.objects.filter(user_id=userIdOrError).first()
    if not userObj:
        return JsonResponse({"Message": "User not found"}, status=404)

    profileObj = profile.objects.filter(
        user_id=userObj,
        is_active=True,
        is_deleted=False
    ).first()

    if not profileObj:
        return JsonResponse({"Message": "Profile not found"}, status=404)

    profileObj.is_deleted = True
    profileObj.is_active = False
    profileObj.save()

    return JsonResponse({"Message": "Profile deleted successfully"}, status=200)
    
#SIZE API
@csrf_exempt
@api_view(['POST'])
def CreateSize(request):
    try:
        sizeName = request.data.get("sizeName")
        parentId = request.data.get("parentId")
        print(parentId)
        if not sizeName:
            return JsonResponse({"message":"add right size name!!"},status=400)
        try:
            sizeObj= size.objects.get(size_id=parentId)
            print(sizeObj)
        except size.DoesNotExist:
            return JsonResponse({"message":"size not found!!!"},status=404)
        
        size.objects.create(
            size_name=sizeName,
            parent_size=sizeObj
        )
        return JsonResponse({"message":"size created"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500) 
    
# 20)CATEGORY API
@csrf_exempt  
@api_view(["POST"])
def createCategory(request):
    try:
        categoryName = request.data.get("categoryName")
        categoryImage = request.data.get("categoryImage")
        isActive = request.data.get("isActive")
        parentId = request.data.get("parentId")
        print(parentId)
 
        if not categoryName:
            return JsonResponse({"message":"enter valid name!"},status=400)
        if not categoryImage:
                return JsonResponse({"message":"add image!!"},status=400)
        parentCategoryObj=None
        if parentId:
            try:
                parentCategoryObj=category.objects.get(category_id=parentId)
            except category.DoesNotExist:
                return JsonResponse({"message":"parent category not found!!"},status=404)
       
        category.objects.create(
            category_name=categoryName,
            category_image=categoryImage,
            is_active=isActive,
            parent_category = parentCategoryObj
        )
        return JsonResponse({"message":"category created"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
 
# 21)  GET ALL CATEGORY
@csrf_exempt
@api_view(["GET"])
def getAllCategory(request):
    try:
        categories = category.objects.all()
 
        data = []
        for cat in categories:
            data.append({
                "categoryId": cat.category_id,
                "categoryName": cat.category_name,
                "isActive": cat.is_active,
                "categoryImage": request.build_absolute_uri(cat.category_image.url)
            })
 
        return JsonResponse({"data": data}, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
#22) GET SINGLE CATEGORY
@csrf_exempt
@api_view(["GET"])
def getSingleCategory(request):
    try:
        CategoryId = request.GET.get("CategoryId")
        if not CategoryId:
            return JsonResponse({"message":"pls send category ID!!"},status=400)
        try:
            categoryObj = category.objects.get(category_id=CategoryId)
        except category.DoesNotExist:
            return JsonResponse({"message":"category not found!!"},status=404)
        data={
            "categoryId":categoryObj.category_id,
            "categoryName":categoryObj.category_name,
            "isActive":categoryObj.is_active,
            "categoryImage": request.build_absolute_uri(categoryObj.category_image.url)
        }
        return JsonResponse({"data": data}, status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)
 
 
# 23)PRODUCT API
@csrf_exempt
@api_view(["POST"])
def createProduct(request):
    try:
        productName = request.data.get("productName")
        shortDescription = request.data.get("shortDescription")
        Description = request.data.get("Description")
        Category = request.data.get("Category")
        Price = request.data.get("Price")
        isActive = request.data.get("isActive")
        Color = request.data.get("Color")
        Size = request.data.getlist("Size")
        images = request.data.getlist("images")
 
        if not Size:
            return JsonResponse({"message": "select size"}, status=400)
 
        try:
            categoryObj = category.objects.get(category_id=Category)
        except category.DoesNotExist:
            return JsonResponse({"message": "category not found"}, status=404)
 
        sizeObjs = size.objects.filter(size_id__in=Size)
 
        if not sizeObjs.exists():
            return JsonResponse({"message": "size not found"}, status=404)
       
 
        productObj = product.objects.create(
            product_name=productName,
            short_description=shortDescription,
            description=Description,
            category=categoryObj,
            price=Price,
            is_active=isActive
        )
        colorObjs = color.objects.filter(color_name__in=Color)
        productObj.color.set(colorObjs)
 
        # MANY TO MANY SET
        productObj.size.set(sizeObjs)
 
        for image in images:
            productImages.objects.create(
            product_id=productObj,
            images=image
        )
        return JsonResponse({"message": "product created successfully"}, status=201)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
   
#24)PRODUCT GET ALL API
@csrf_exempt
@api_view(["GET"])
def getAllProduct(request):
    try:
        products = product.objects.filter(is_active=True)
        related = request.GET.get("related")
        productId = request.GET.get("productId")
        search = request.GET.get("search")
        color = request.GET.get("color")
        

        if search:
            products = products.filter(product_name__icontains=search)
        if related == "true" and productId:
            try:
                current = product.objects.get(
                    product_id=productId,
                    is_active=True
                )
            except product.DoesNotExist:
                return JsonResponse({"total": 0, "data": []})

            final_products = []
            used_ids = [current.product_id]

            same_cat_same_color = product.objects.filter(
                category=current.category,
                color__color_name__iexact=current.color.first().color_name,
                is_active=True
            ).exclude(product_id__in=used_ids)[:3]

            final_products.extend(same_cat_same_color)
            used_ids.extend([p.product_id for p in same_cat_same_color])

            same_cat_diff_color = product.objects.filter(
                category=current.category,
                is_active=True
            ).exclude(
                color__color_name__iexact=current.color.first().color_name
            ).exclude(
                product_id__in=used_ids
            )[:3]

            final_products.extend(same_cat_diff_color)
            used_ids.extend([p.product_id for p in same_cat_diff_color])

            diff_category = product.objects.filter(
                is_active=True
            ).exclude(
                category=current.category
            ).exclude(
                product_id__in=used_ids
            )[:2]

            final_products.extend(diff_category)

            data = []
            for prod in final_products[:8]:
                if color:
                    imageObj = productImages.objects.filter(
                        product_id=prod,
                        color__color_name__iexact=color
                    ).first()
                else:
                    imageObj = productImages.objects.filter(product_id=prod).first()
                imageUrl = (
                    request.build_absolute_uri(imageObj.images.url)
                    if imageObj else ""
                )

                data.append({
                    "productId": prod.product_id,
                    "productName": prod.product_name,
                    "price": prod.price,
                    "color": [c.color_name for c in prod.color.all()],
                    "image": imageUrl
                })

            return JsonResponse({
                "total": len(data),
                "data": data
            })

        # =====================================
        # 🔹 NORMAL + CHATBOT LOGIC
        # =====================================

        startRange = request.GET.get("startRange")
        endRange = request.GET.get("endRange")
        sort = request.GET.get("sort")
        # color = request.GET.get("color")
        categoryId = request.GET.get("categoryId")
        searchQuery = request.GET.get("searchQuery")
        chat_category = request.GET.get("chatCategory")
        tone = request.GET.get("tone")
        body = request.GET.get("body")
        size = request.GET.get("size")

        if size:
            products = products.filter(size__size_name__iexact=size).distinct()

        BODY_RULES = {
            "pear": {
                "allow": ["wide", "bell", "flare", "high-waist"],
                "avoid": ["slim"]
            },
            "apple": {
                "allow": ["wrap", "layered", "maxi"],
                "avoid": ["slim"]
            },
            "hourglass": {
                "allow": ["wrap", "flare", "knot"],
                "avoid": []
            },
            "rectangle": {
                "allow": ["ruffle", "layered", "knot"],
                "avoid": []
            },
            "inverted triangle": {
                "allow": ["wide", "flare"],
                "avoid": []
            }
        }

        if startRange:
            products = products.filter(price__gte=startRange)

        if endRange:
            products = products.filter(price__lte=endRange)

        if color:
            products = products.filter(color__color_name__iexact=color)

        if categoryId:
            products = products.filter(category_id=categoryId)

        if searchQuery:
            products = products.filter(product_name__icontains=searchQuery)

        # 🔥 CHATBOT CATEGORY
        if chat_category:
            products = products.filter(
                category__category_name__icontains=chat_category
            )

        # 🔥 CHATBOT TONE
        if tone:
            cool_colors = ["BLUE", "PURPLE", "GREY", "SILVER", "BLACK"]
            warm_colors = ["RED", "ORANGE", "YELLOW", "BEIGE", "BROWN"]

            if tone.lower() == "cool":
                products = products.filter(color__color_name__in=cool_colors)

            elif tone.lower() == "warm":
                products = products.filter(color__color_name__in=warm_colors)

            
        if body and body in BODY_RULES and not tone:

            rules = BODY_RULES[body]

            allow_words = rules["allow"]
            avoid_words = rules["avoid"]

            allow_query = Q()
            for word in allow_words:
                allow_query |= Q(product_name__icontains=word)

            avoid_query = Q()
            for word in avoid_words:
                avoid_query |= Q(product_name__icontains=word)

            products = products.filter(allow_query)

            if avoid_words:
                products = products.exclude(avoid_query)

        if sort == "new":
            products = products.order_by("-created_at")
        elif sort == "price_low":
            products = products.order_by("price")
        elif sort == "price_high":
            products = products.order_by("-price")

        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 8))

        totalProducts = products.count()
        start = (page - 1) * limit
        end = start + limit
        products = products[start:end]

        data = []
        for prod in products:
            colorImages = []

            for c in prod.color.all():
                img = productImages.objects.filter(product_id=prod, color=c).first()

                colorImages.append({
                    "color": c.color_name,
                    "code": c.color_code,
                    "image": request.build_absolute_uri(img.images.url) if img else ""
                })
            if color:
                imageObj = productImages.objects.filter(
                    product_id=prod,
                    color__color_name__iexact=color
                ).first()
            else:
                imageObj = productImages.objects.filter(product_id=prod).first()
            imageUrl = (
                request.build_absolute_uri(imageObj.images.url)
                if imageObj else ""
            )

            data.append({
                "productId": prod.product_id,
                "productName": prod.product_name,
                "price": prod.price,
                "colors": [
                    {
                        "name": c.color_name,
                        "code": c.color_code
                    }
                    for c in prod.color.all()
                ],
                "image": imageUrl,
                "colorImages": colorImages
            })

        return JsonResponse({
            "total": totalProducts,
            "page": page,
            "limit": limit,
            "data": data
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
#25)GET PRODUCT BY ID API
@csrf_exempt
@api_view(['GET'])
def getSingleProduct(request):
    try:
        productID = request.GET.get("productID")
        if not productID:
            return JsonResponse({"message": "please enter valid id"}, status=400)

        try:
            prodObj = product.objects.get(product_id=productID)
        except product.DoesNotExist:
            return JsonResponse({"message": "product not found"}, status=404)

        # image
        colorId = request.GET.get("colorId")

        print("RAW colorId:", colorId)

        if colorId:
            colorId = int(colorId)

            imageObj = productImages.objects.filter(
                product_id=prodObj,
                color__color_id=colorId
            ).order_by("image_id")

            print("FILTERED IMAGES:", imageObj)

            if not imageObj.exists():
                print("No images found for this color")

        else:
            print("NO COLOR ID → using default")

            first_image = productImages.objects.filter(product_id=prodObj).first()

            if first_image:
                imageObj = productImages.objects.filter(
                    product_id=prodObj,
                    color=first_image.color
                ).order_by("image_id")
            else:
                imageObj = []


        defaultColor = None
        first_img = imageObj.first()

        if first_img:
            defaultColor = first_img.color.color_id
                
        
        imageList = [
            request.build_absolute_uri(img.images.url)
            for img in imageObj
        ]

        # SIZE + STOCK STATUS
        sizeList = []
        productSizes = prodObj.size.all()

        # ensure colorId exists
        if not colorId:
            colorId = defaultColor

        for sizeObj in productSizes:

            stockObj = stock.objects.filter(
                product_id=prodObj,
                color_id=colorId,
                size_id=sizeObj
            ).first()

            stockQty = 0
            if stockObj:
                stockQty = stockObj.stock_quantity

            sizeList.append({
                "size": sizeObj.size_name,
                "stock_quantity": stockQty,
                "in_stock": stockQty > 0
            })
        infoObj = additionalInformation.objects.filter(product_id=prodObj)

        additionalInfoList = []

        for info in infoObj:
            additionalInfoList.append({
                "label": info.label,
                "label_data": info.label_data
            })

        # COLORS
        colorList = []

        for c in prodObj.color.all():
            colorList.append({
                "color_id": c.color_id,
                "color_name": c.color_name,
                "color_code": c.color_code
            })

        prodData = {
            "id": prodObj.product_id,
            "name": prodObj.product_name,
            "shortdesc": prodObj.short_description,
            "description": prodObj.description,
            "category_id": prodObj.category.category_id,
            "category_name": prodObj.category.category_name,
            "sizes": sizeList,
            "price": prodObj.price,
            "is_active": prodObj.is_active,
            "colors": colorList,
            "selected_color": defaultColor,
            "image": imageList,
            "additional_information": additionalInfoList
        }


        return JsonResponse({"data": prodData}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
#PRODUCTIMAGE API
@csrf_exempt
@api_view(["POST"])
def productImage(request):
    try:
        Images = request.FILES.get("Images")
        productId = request.data.get("productId")
       
        try:
            productObj = product.objects.get(product_id=productId)
        except product.DoesNotExist:
            return JsonResponse({"message":"product not found!!"},status=404)
        productImages.objects.create(
            images = Images,
            product_id=productObj
        )
        return JsonResponse({"message":"image added successfully!"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)

#ADDRESS API
@csrf_exempt
@api_view(["POST"])  
def addAddress(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error":"Please login first!!"}, status=400)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error":"User not found"}, status=404)


        streetAddress = request.data.get("streetAddress")
        Landmark = request.data.get("Landmark")
        Pincode =request.data.get("Pincode")
        userId = request.data.get("userId")
        isActive = request.data.get("isActive")
        fullName = request.data.get("fullName")
        dialCode = request.data.get("dialCode")
        phoneNumber =request.data.get("phoneNumber")
 
        if not streetAddress:
            return JsonResponse({"message":"enter valid Address!!"},status=400)
        if not Landmark:
            return JsonResponse({"enter valid Landmark!!"},status=400)
       
        try:
            pincodeObj = pincode.objects.get(pincode=Pincode)
        except pincode.DoesNotExist:
            return JsonResponse({"message":"pincode not found!!"},status=404)
       
       
        if not fullName:
            return JsonResponse({"message":"enter full name"},status=400)
        if not dialCode:
            return JsonResponse({"message":"enter dial code of your country"},status=400)
        if not phoneNumber or len(phoneNumber)>=11:
            return JsonResponse({"message":"enter valid phone number!!"},status=400)
       
        address.objects.create(
        street_address=streetAddress,
        landmark=Landmark,
        pincode=pincodeObj,
        user_id=userObj,
        is_active=isActive,
        full_name=fullName,
        dial_code=dialCode,
        phone_number=phoneNumber
        )
        return JsonResponse({"message":"Address Saved!!"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)

# 32)GET SINGLE ADDRESS
@csrf_exempt
@api_view(["GET"])
def getAllAddressesOfUser(request):
 
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error":"Please login first!!"}, status=400)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error":"User not found"}, status=404)
 
        addressList = address.objects.filter(user_id=userObj, is_active=True)
        if not addressList.exists():
            return JsonResponse({"data": []}, status=200)
 
 
        if not addressList:
            return JsonResponse({"message": "address not found!!"}, status=404)
 
        data = []
        for addr in addressList:
            data.append({
                "addressId": addr.address_id,
                "userId": addr.user_id.user_id,
                "streetAddress": addr.street_address,
                "landmark": addr.landmark,
                "pincode": addr.pincode.pincode,
                "isActive": addr.is_active,
                "fullName": addr.full_name,
                "dialCode": addr.dial_code,
                "phoneNumber": addr.phone_number
            })
 
        return JsonResponse({"data":data}, status=200)
 
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)
   
  
 
    
# UPDATE ADDRESS 
@csrf_exempt
@api_view(["POST"])
def updateAddress(request):
    try:
        addressId = request.data.get("addressId")

        if not addressId:
            return JsonResponse({"message":"Please send addressId!"}, status=400)

        try:
            addressObj = address.objects.get(address_id=addressId, is_active=True)
        except address.DoesNotExist:
            return JsonResponse({"message":"Address not found!"}, status=404)

        # Update fields only if provided
        streetAddress = request.data.get("streetAddress")
        landmark = request.data.get("landmark")
        pincode = request.data.get("pincode")
        fullName = request.data.get("fullName")
        dialCode = request.data.get("dialCode")
        phoneNumber = request.data.get("phoneNumber")

        if streetAddress:
            addressObj.street_address = streetAddress

        if landmark:
            addressObj.landmark = landmark

        if pincode:
            addressObj.pincode = pincode

        if fullName:
            addressObj.full_name = fullName

        if dialCode:
            addressObj.dial_code = dialCode

        if phoneNumber:
            addressObj.phone_number = phoneNumber

        addressObj.save()

        return JsonResponse({"message":"Address updated successfully!"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# REMOVE ADDRESS
@csrf_exempt
@api_view(["POST"])
def removeAddress(request):
    try:
        addressId = request.data.get("addressId")

        if not addressId:
            return JsonResponse({"message": "Please send addressId!"}, status=400)

        try:
            addressObj = address.objects.get(address_id=addressId, is_active=True)
        except address.DoesNotExist:
            return JsonResponse({"message": "Address not found!"}, status=404)

        addressObj.is_active = False
        addressObj.save()

        return JsonResponse({"message": "Address removed successfully!"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

#33) GET SINGLE ADDRESS
@csrf_exempt
@api_view(["GET"])
def getSingleAddress(request):
    try:
        addressId = request.GET.get("addressId")
        if not addressId:
            return JsonResponse({"message":"pls send address ID!!"}, status=400)

        try:
            addressObj = address.objects.get(address_id=addressId, is_active=True)
        except address.DoesNotExist:
            return JsonResponse({"message":"address not found!!"}, status=404)

        data = {
            "addressId": addressObj.address_id,
            "userId": addressObj.user_id.user_id,
            "streetAddress": addressObj.street_address,
            "landmark": addressObj.landmark,
            "pincode": addressObj.pincode.Pincode,
            "isActive": addressObj.is_active,
            "fullName": addressObj.full_name,
            "dialCode": addressObj.dial_code,
            "phoneNumber": addressObj.phone_number
        }

        return JsonResponse({"data":data}, status=200)

    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)

#update order address
@csrf_exempt
@api_view(["POST"])
def updateOrderAddress(request):
 
    try:
 
        serialNo = request.data.get("serialNo")
        addressId = request.data.get("addressId")
 
        if not serialNo or not addressId:
            return JsonResponse({"message":"Missing data"},status=400)
 
        orderObj = order.objects.get(serial_no=serialNo)
        addressObj = address.objects.get(address_id=addressId)
 
        # update order address
        orderObj.address_id = addressObj
        orderObj.save()
 
        # get user from order
        userObj = orderObj.user_id
 
        # save order history
        orderHistory.objects.create(
            order_id = orderObj,
            user_id = userObj,
            address_id = addressObj,
            message = "Delivery address changed"
        )
 
        return JsonResponse({"message":"Address updated successfully"},status=200)
 
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
 
 

# 35) ADD TO CART
@csrf_exempt
@api_view(["POST"])
def addToCart(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Please login first!!"}, status=400)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error": "User not found"}, status=404)
 
        # DATA
        productId = request.data.get("productId")
        quantity = int(request.data.get("quantity", 1))
        sizeId = request.data.get("sizeId")   # ✅ SHOULD BE size_id
        colorId = request.data.get("colorId")
 
        if not productId:
            return JsonResponse({"error": "productId is required"}, status=400)
 
        if not colorId:
            return JsonResponse({"error": "Please select color"}, status=400)
 
        # PRODUCT
        try:
            productObj = product.objects.get(product_id=productId)
        except product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
 
        # COLOR
        try:
            colorObj = color.objects.get(color_id=colorId)
        except color.DoesNotExist:
            return JsonResponse({"error": "Invalid color"}, status=400)
        
        # SIZE
        if sizeId:
            try:
                sizeObj = size.objects.get(size_id=sizeId)
            except size.DoesNotExist:
                return JsonResponse({"message": "size not found"}, status=404)
        else:
            stockObj = stock.objects.filter(
                product_id=productObj,
                color_id=colorObj,
                stock_quantity__gt=0
            ).first()

            if not stockObj:
                return JsonResponse({"error": "Product is out of stock"}, status=400)

            sizeObj = stockObj.size_id
 
        # SIZE (✅ FIXED: use size_id instead of name)
        if sizeId:
            try:
                sizeObj = size.objects.get(size_id=sizeId)
            except size.DoesNotExist:
                return JsonResponse({"message":"size not found"}, status=404)
        else:
            # pick first available size from stock
            stockObj = stock.objects.filter(
                product_id=productObj,
                color_id=colorObj,
                stock_quantity__gt=0
            ).first()

            if not stockObj:
                return JsonResponse({"error":"Product is out of stock"}, status=400)

            sizeObj = stockObj.size_id
 
        # QUANTITY CHECK
        if quantity <= 0:
            return JsonResponse(
                {"error": "You have to add at least 1 quantity"}, status=400
            )
 
        # ✅ STOCK CHECK (FIXED)
        stockObj = stock.objects.filter(
            product_id=productObj,
            size_id=sizeObj,
            color_id=colorObj
        ).first()
 
        if not stockObj or stockObj.stock_quantity <= 0:
            return JsonResponse(
                {"error": "Product is out of stock"}, status=400
            )
 
        # Check quantity limit
        if quantity > stockObj.stock_quantity:
            return JsonResponse(
                {"error": f"Only {stockObj.stock_quantity} items left in stock"},
                status=400
            )
 
        # CREATE CART
        cartObj = cart.objects.filter(user_id=userObj, is_active=True).first()
        if not cartObj:
            cartObj = cart.objects.create(
                user_id=userObj, is_active=True, grand_total=0
            )
 
        # CHECK EXISTING ITEM
        cartItemObj = cartItems.objects.filter(
            cart_id=cartObj,
            product_id=productObj,
            size=sizeObj,
            color=colorObj
        ).first()
 
        if cartItemObj:
            newQuantity = cartItemObj.quantity + quantity
 
            if newQuantity > stockObj.stock_quantity:
                return JsonResponse(
                    {"error": f"Only {stockObj.stock_quantity} items available"},
                    status=400
                )
 
            cartItemObj.quantity = newQuantity
            cartItemObj.total = cartItemObj.price * cartItemObj.quantity
            cartItemObj.save()
 
        else:
            cartItems.objects.create(
                cart_id=cartObj,
                product_id=productObj,
                quantity=quantity,
                price=productObj.price,
                size=sizeObj,
                color=colorObj,
                total=productObj.price * quantity,
            )
 
        # UPDATE CART TOTAL
        cartItemsList = cartItems.objects.filter(cart_id=cartObj)
        grandTotal = 0
 
        for item in cartItemsList:
            item.total = item.price * item.quantity
            item.save()
            grandTotal += item.total
 
        cartObj.grand_total = grandTotal
        cartObj.save()
 
        return JsonResponse({"message": "Product added to cart"}, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
 
# 36) REMOVE CART ITEM
@csrf_exempt
@api_view(["POST"])
def removeCartItem(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Please login first!!"}, status=400)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error": "User not found"}, status=404)
 
        # DATA
        cartItemId = request.data.get("cartItemId")
        if not cartItemId:
            return JsonResponse({"message": "cartItemId required"}, status=400)
 
        try:
            cartItemObj = cartItems.objects.get(
                cart_item_id=cartItemId,
                cart_id__user_id=userObj,
                cart_id__is_active=True,
            )
        except cartItems.DoesNotExist:
            return JsonResponse({"message": "Cart item not found"}, status=404)
 
        cartObj = cartItemObj.cart_id
 
        # DELETE ITEM
        cartItemObj.delete()
 
        # UPDATE CART TOTAL
        cartItemsList = cartItems.objects.filter(cart_id=cartObj)
 
        grandTotal = 0
        for item in cartItemsList:
            grandTotal += item.price * item.quantity
 
        cartObj.grand_total = grandTotal
        cartObj.save()
 
        return JsonResponse({"message": "Item removed from cart"}, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
 
# 37)GET ALL CART
@csrf_exempt
@api_view(["GET"])
def getAllCart(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Please login first!!"}, status=400)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error": "User not found"}, status=404)
 
        cartObj = cart.objects.filter(user_id=userObj, is_active=True).first()
        if not cartObj:
            return JsonResponse({"grandTotal": 0, "items": []})
 
        cartItemsList = cartItems.objects.filter(cart_id=cartObj)
 
        items = []
        for item in cartItemsList:
            prod = item.product_id
        
            # ✅ CORRECT: stock table
            productSizes = stock.objects.filter(product_id=prod).values(
                "size_id__size_name",
                "stock_quantity"
            )
 
            imageObj = productImages.objects.filter(
                product_id=prod,
                color=item.color
            ).first()

            # fallback if color image not found
            if not imageObj:
                imageObj = productImages.objects.filter(product_id=prod).first()
            imageUrl = request.build_absolute_uri(imageObj.images.url) if imageObj else ""
 
            items.append({
                "cartItemId": item.cart_item_id,
                "productId": prod.product_id,
                "productName": prod.product_name,
                "price": item.price,
                "quantity": item.quantity,
                "totalPrice": item.price * item.quantity,
                "image": imageUrl,
                "selectedSize": item.size.size_name if item.size else "",
                "sizes": list(productSizes)
            })
 
        return JsonResponse(
            {"grandTotal": cartObj.grand_total, "items": items},
            status=200
        )
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
# 38)get single cart
@csrf_exempt
@api_view(["GET"])
def getSingleCart(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Please login first!!"}, status=400)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error": "User not found"}, status=404)
 
        # GET cartItemId
        cartItemId = request.GET.get("cartItemId")
        if not cartItemId:
            return JsonResponse({"message": "cartItemId required"}, status=400)
 
        try:
            cartItemObj = cartItems.objects.get(
                cart_item_id=cartItemId,
                cart_id__user_id=userObj,
                cart_id__is_active=True,
            )
        except cartItems.DoesNotExist:
            return JsonResponse({"message": "Cart item not found"}, status=404)
 
        prod = cartItemObj.product_id
 
        # IMAGE
        imageObj = productImages.objects.filter(product_id=prod).first()
        if imageObj:
            imageUrl = request.build_absolute_uri(imageObj.images.url)
        else:
            imageUrl = ""
 
        data = {
            "cartItemId": cartItemObj.cart_item_id,
            "productId": prod.product_id,
            "productName": prod.product_name,
            "price": cartItemObj.price,
            "quantity": cartItemObj.quantity,
            "totalPrice": cartItemObj.price * cartItemObj.quantity,
            "image": imageUrl,
        }
 
        return JsonResponse(data, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
 
# 39) remove cart
@csrf_exempt
@api_view(["POST"])
def removeCart(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Please login first!!"}, status=400)
 
        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)
 
        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error": "User not found"}, status=404)
 
        # GET ACTIVE CART
        cartObj = cart.objects.filter(user_id=userObj, is_active=True).first()
        if not cartObj:
            return JsonResponse({"message": "Cart is already empty"}, status=400)
 
        # DELETE ALL CART ITEMS
        cartItems.objects.filter(cart_id=cartObj).delete()
 
        # RESET CART TOTAL
        cartObj.grand_total = 0
        cartObj.save()
 
        return JsonResponse({"message": "Cart cleared successfully"}, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
 
# QUANTITY PLUS OT MINUS
@csrf_exempt
@api_view(["POST"])
def cartItemQuantityPlusOrMinus(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error": "Please login first!!"}, status=400)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error": "User not found"}, status=404)

        # DATA
        cartItemId = request.data.get("cartItemId")
        action = request.data.get("action")

        if not cartItemId or not action:
            return JsonResponse(
                {"message": "cartItemId and action required"}, status=400
            )

        try:
            cartItemObj = cartItems.objects.get(
                cart_item_id=cartItemId, cart_id__user_id=userObj
            )
        except cartItems.DoesNotExist:
            return JsonResponse({"message": "Cart item not found"}, status=404)

        # STOCK CHECK FOR PLUS ACTION
        if action == "plus":
            try:
                stockObj = stock.objects.get(
                    product_id=cartItemObj.product_id,
                    size_id=cartItemObj.size
                )
            except stock.DoesNotExist:
                return JsonResponse(
                    {"error": "Product is out of stock"}, status=400
                )

            # check if next quantity exceeds stock
            if cartItemObj.quantity + 1 > stockObj.stock_quantity:
                return JsonResponse(
                    {
                        "error": f"Only {stockObj.stock_quantity} items available in stock"
                    },
                    status=400,
                )

            cartItemObj.quantity += 1
            cartItemObj.save()

        elif action == "minus":
            if cartItemObj.quantity > 1:
                cartItemObj.quantity -= 1
                cartItemObj.save()
            else:
                cartItemObj.delete()
                
                # cart total after delete
                cartObj = cartItemObj.cart_id
                cartItemsList = cartItems.objects.filter(cart_id=cartObj)
                grandTotal = sum(item.price * item.quantity for item in cartItemsList)
                cartObj.grand_total = grandTotal
                cartObj.save()
                return JsonResponse(
                    {"message": "Item removed from cart"}, status=200
                )

        else:
            return JsonResponse({"message": "Invalid action"}, status=400)

        # UPDATE ITEM TOTAL
        cartItemObj.total = cartItemObj.price * cartItemObj.quantity
        cartItemObj.save()

        # UPDATE CART TOTAL
        cartObj = cartItemObj.cart_id
        cartItemsList = cartItems.objects.filter(cart_id=cartObj)

        grandTotal = 0
        for item in cartItemsList:
            grandTotal += item.price * item.quantity

        cartObj.grand_total = grandTotal
        cartObj.save()

        return JsonResponse({"message": "Quantity updated successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# 49) get wishlist by id
@csrf_exempt
@api_view(["GET"])
def getWishlistByUserId(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Please login first"}, status=401)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        userObj = user.objects.get(user_id=userIdOrError)

        wishlistItems = wishlist.objects.filter(user_id=userObj)

        data = []
        for wish in wishlistItems:
            productObj = wish.product_id
            imageObj = productImages.objects.filter(
                product_id=productObj,
                color=wish.color
            ).first()

            if not imageObj:
                imageObj = productImages.objects.filter(product_id=productObj).first()

            imageUrl = request.build_absolute_uri(imageObj.images.url) if imageObj else ""

            data.append({
                "wishlistId": wish.wishlist_id,
                "productId": productObj.product_id,
                "colorId": wish.color.color_id if wish.color else None, 
                "productName": productObj.product_name,
                "price": productObj.price,
                "image": imageUrl
            })

        return JsonResponse({"data": data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def sendCustomEmail(subject, message, recipient_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        fail_silently=False,
    )

#ORDER API
@csrf_exempt
@api_view(["POST"])
def createOrder(request):
    try:
        # ---------------- TOKEN CHECK ----------------
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        try:
            userObj = user.objects.get(user_id=userIdOrError)
        except user.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)

        # ---------------- INPUT DATA ----------------
        addressId = request.data.get("addressId")
        paymentChoice = int(request.data.get("paymentChoice", 0))  

        try:
            addressObj = address.objects.get(address_id=addressId)
        except address.DoesNotExist:
            return JsonResponse({"message": "Address not found"}, status=404)

        # ---------------- GET ACTIVE CART ----------------
        cartObj = cart.objects.filter(user_id=userObj, is_active=True).first()
        if not cartObj:
            return JsonResponse({"message": "Cart is empty"}, status=400)

        cartItemsList = cartItems.objects.filter(cart_id=cartObj)
        if not cartItemsList.exists():
            return JsonResponse({"message": "No items in cart"}, status=400)

        deliveryCharge = 100
        grandTotal = cartObj.grand_total + deliveryCharge

        # ---------------- STOCK CHECK ----------------
        for item in cartItemsList:
            try:
                stockObj = stock.objects.get(
                    product_id=item.product_id,
                    size_id=item.size
                )
            except stock.DoesNotExist:
                return JsonResponse({
                    "message": f"Stock not found for {item.product_id.product_name}"
                }, status=400)

            if stockObj.stock_quantity < item.quantity:
                return JsonResponse({
                    "message": f"{item.product_id.product_name} ({item.size.size_name}) is out of stock"
                }, status=400)

        # ---------------- PAYMENT CHECK ----------------
        paymentStatus = 0

        if paymentChoice == 1:
            cardNumber = int(request.data.get("cardNumber"))
            cardCvv = int(request.data.get("cardCvv"))
            cardExpiry = int(request.data.get("cardExpiry"))
            if not cardNumber:
                return JsonResponse({"message": "Card number required"}, status=400)

            try:
                cardObj = cardDetail.objects.get(card_number=cardNumber)
            except cardDetail.DoesNotExist:
                return JsonResponse({"message": "Invalid card details"}, status=400)

            if cardCvv != cardObj.card_cvv or cardExpiry != cardObj.card_expiry:
                return JsonResponse({"message": "Invalid card details"}, status=400)

            if grandTotal > cardObj.card_balance:
                return JsonResponse({"message": "Insufficient balance"}, status=400)

           
            paymentStatus = 1
       # ---------------- CREATE ORDER + STOCK + CART (ATOMIC) ----------------
        with transaction.atomic():
            
            if paymentChoice == 1:
                    cardObj.card_balance -= grandTotal
                    cardObj.save()

            orderObj = order.objects.create(
                cart_id=cartObj,
                user_id=userObj,
                grand_total=grandTotal,
                delivery_charges=deliveryCharge,
                status=0,
                payment_choices=paymentChoice,
                payment_status=paymentStatus,
                address_id=addressObj
            )
            for item in cartItemsList:
                orderItems.objects.create(
                    order_id=orderObj,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                    size=item.size,
                    color=item.color
                )

            # Reduce stock
            for item in cartItemsList:
                stockObj = stock.objects.get(
                    product_id=item.product_id,
                    size_id=item.size
                )

                if stockObj.stock_quantity < item.quantity:
                    raise Exception("Stock changed. Try again.")

                stockObj.stock_quantity -= item.quantity
                stockObj.save()

            # Clear cart
            cartItemsList.delete()
            cartObj.is_active = False
            cartObj.save()
        # ---------------- DELIVERY LOGIC ----------------
        orderCity = addressObj.pincode.city_id

        deliveryPersonsInCity = deliveryPerson.objects.filter(city=orderCity)

        if deliveryPersonsInCity.exists():
            
            for dp in deliveryPersonsInCity:
                subject = f"New Order Available - #{orderObj.order_id}"

                message = f"""
                New Order Available!

                Order ID: {orderObj.order_id}
                Customer: {orderObj.user_id.username},
                Address: {orderObj.address_id.street_address}, 
                {orderObj.address_id.landmark}, 
                {orderObj.address_id.pincode.pincode}, 
                {orderObj.address_id.pincode.city_id.city_name}
                Total: {orderObj.grand_total}

                Click here to accept:
                http://127.0.0.1:8000/accept/{orderObj.order_id}/
                """

                sendCustomEmail(subject, message, dp.email)

        else:
            orderObj.status = 8  
            orderObj.save()
        return JsonResponse({
            "message": "Order placed successfully",
            "orderId": orderObj.order_id
            }, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
            
# 41)GET CURRENT ORDER:
@csrf_exempt
@api_view(["GET"])
def getCurrentOrder(request):
    try:
        # TOKEN
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"error":"Please login first!!"}, status=400)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        userObj = user.objects.filter(user_id=userIdOrError).first()
        if not userObj:
            return JsonResponse({"error":"User not found"}, status=404)

        orderList = order.objects.filter(
            user_id=userObj
        ).exclude(status=1)

        data = []

        for ord in orderList:
            data.append({
                "orderId": ord.order_id,
                "cartId": ord.cart_id.cart_id,
                "grandTotal": ord.grand_total,
                "status": ord.status,
                "addressId": ord.address_id.address_id,
            })

        return JsonResponse({"data": data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

#42) GET ORDER HISTORY
@csrf_exempt
@api_view(["GET"])
def getOrderHistory(request):
 
    try:
 
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message":"Login required"},status=401)
 
        userId = verifyToken(token)
        userObj = user.objects.get(user_id=userId) 
        orders = order.objects.filter(user_id=userObj).order_by("-order_id")
 
        data = [] 
        for ord in orders: 
            items = orderItems.objects.filter(order_id=ord)
            items_list = []
            for item in items:
                img = productImages.objects.filter(
                    product_id=item.product_id,
                    color=item.color
                ).first()

                if not img:
                    img = productImages.objects.filter(
                        product_id=item.product_id
                    ).first()

                image = img.images.url if img else ""
                items_list.append({
                    "productName": item.product_id.product_name,
                    "quantity": item.quantity,
                    "size": item.size.size_name if item.size else "",
                    "price": item.price,
                    "image": image
                })
 
            data.append({
 
                "serialNo": ord.serial_no,
                "status": ord.get_status_display(),
                "deliveryDate": ord.created_at.strftime("%d %b %Y"),
                "grandTotal": ord.grand_total,
                "items": items_list
 
            })
 
        return JsonResponse({"data":data})
 
    except Exception as e:
        return JsonResponse({"error":str(e)})
 

# 43) GET ORDER HISTORY BY ID
@csrf_exempt
@api_view(["GET"])
def getOrderHistoryById(request):
 
    try:
 
        serialNo = request.GET.get("serialNo")
 
        if not serialNo:
            return JsonResponse({"message": "serialNo is required"}, status=400)
 
        try:
            orderObj = order.objects.get(serial_no=serialNo)
        except order.DoesNotExist:
            return JsonResponse({"message": "order not found"}, status=404)
 
 
        # -------- ORDER ITEMS --------
 
        items = orderItems.objects.filter(order_id=orderObj)
 
        itemList = []
 
        for item in items:
 
            img = productImages.objects.filter(
                product_id=item.product_id,
                color=item.color
            ).first()

            if not img:
                img = productImages.objects.filter(
                    product_id=item.product_id
                ).first()
 
            image = img.images.url if img else ""
 
            itemList.append({
                "productID": item.product_id.product_id,
                "productName": item.product_id.product_name,
                "quantity": item.quantity,
                "size": item.size.size_name if item.size else "",
                "price": item.price,
                "image": image
 
            })
 
 
        # -------- ADDRESS --------
 
        addr = orderObj.address_id
 
 
        # -------- ORDER HISTORY TRACKING --------
 
        history = orderHistory.objects.filter(order_id=orderObj)
 
        ordered_date = orderObj.created_at.strftime("%d %b")
 
        shipped_date = None
        out_date = None
        delivered_date = None
 
        for h in history:
 
            msg = h.message.lower()
 
            if "accepted" in msg:
                shipped_date = h.created_at.strftime("%d %b")
 
            if "out for delivery" in msg:
                out_date = h.created_at.strftime("%d %b")
 
            if "delivered" in msg:
                delivered_date = h.created_at.strftime("%d %b")
 
 
        # -------- FINAL RESPONSE --------
 
        data = {
            "orderID": orderObj.order_id,
            "serialNo": orderObj.serial_no,
 
            "status": orderObj.get_status_display(),
 
            "orderedDate": ordered_date,
            "shippedDate": shipped_date,
            "outForDeliveryDate": out_date,
            "deliveredDate": delivered_date,
 
            "grandTotal": orderObj.grand_total,
 
            "items": itemList,
 
            "address": {
 
                "name": addr.full_name,
                "street": addr.street_address,
                "landmark": addr.landmark,
                "pincode": addr.pincode.pincode,
                "phone": addr.phone_number
 
            }
 
        }
 
        return JsonResponse({"data": data})
 
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
 
 
# review 
   
@csrf_exempt
@api_view(['POST'])
def CreateReviewWithImage(request):
    try:
        # ================= TOKEN =================
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message":"token is required"},status=401)
 
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            userID = payload.get("user_id")
        except Exception:
            return JsonResponse({"message":"Invalid token"},status=401)
 
        # ================= REVIEW DATA =================
        productID = request.data.get("productID")
        orderID = request.data.get("orderID")
        Rating = request.data.get("Rating")
        Comment = request.data.get("Comment")
 
        if not productID:
            return JsonResponse({"message":"productID is required"},status=400)
 
        if not orderID:
            return JsonResponse({"message":"orderID is required"},status=400)
 
        if not Rating:
            return JsonResponse({"message":"Rating is required"},status=400)
 
        if not Comment:
            return JsonResponse({"message":"Comment is required"},status=400)
 
        if not str(Rating).isdigit():
            return JsonResponse({"message":"rating must be digit"},status=400)
 
        Rating = int(Rating)
 
        if Rating not in [1,2,3,4,5]:
            return JsonResponse({"message":"rating must be between 1 and 5"},status=400)
 
        # ================= FETCH OBJECTS =================
        try:
            productObj = product.objects.get(product_id=productID)
        except product.DoesNotExist:
            return JsonResponse({"message":"product not found"},status=404)
 
        try:
            orderObj = order.objects.get(order_id=orderID)
        except order.DoesNotExist:
            return JsonResponse({"message":"order not found"},status=404)
 
        try:
            userObj = user.objects.get(user_id=userID)
        except user.DoesNotExist:
            return JsonResponse({"message":"user not found"},status=404)
 
        # ================= CREATE REVIEW =================
        reviewObj = review.objects.create(
            product_id=productObj,
            order_item_id=orderObj,
            user_id=userObj,
            rating=Rating,
            comment=Comment
        )
 
        # ================= IMAGE PART =================
        Image = request.FILES.get("Image")
 
        if Image:
            reviewImage.objects.create(
                image=Image,
                review_id=reviewObj
            )
 
        # ================= RESPONSE =================
        return JsonResponse({
            "message": "review created successfully",
            "review_id": reviewObj.pk,
            "image_uploaded": True if Image else False
        }, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt   
@api_view(["GET"])
def GetReview(request):
 
    productID = request.GET.get("productID")
    orderID = request.GET.get("orderID")
 
    token = request.headers.get("token")
 
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    userID = payload.get("user_id")
 
    try:
 
        reviewObj = review.objects.get(
            product_id=productID,
            order_item_id=orderID,
            user_id=userID
        )
 
        return JsonResponse({
            "rating": reviewObj.rating,
            "comment": reviewObj.comment
        })
 
    except review.DoesNotExist:
 
        return JsonResponse({
            "rating": 0
        })
       
 
 
#46) REVIEW BY PRODUCT ID
@csrf_exempt
@api_view(["GET"])
def getReviewByProductId(request):
    try:
        productID = request.GET.get("productID")
 
        if not productID:
            return JsonResponse({"message": "productID is required"}, status=400)
 
        try:
            productObj = product.objects.get(product_id=productID)
        except product.DoesNotExist:
            return JsonResponse({"message": "product not found"}, status=404)
 
        reviewList = review.objects.filter(product_id=productObj)
 
        data = []
 
        for rev in reviewList:

            # ✅ GET PROFILE
            try:
                profileObj = profile.objects.filter(user_id=rev.user_id).first()                
                full_name = f"{profileObj.first_name} {profileObj.last_name}"
                profile_image = request.build_absolute_uri(profileObj.profile_picture.url) if profileObj.profile_picture else None
            except profile.DoesNotExist:
                full_name = rev.user_id.username   # fallback
                profile_image = None

            images = reviewImage.objects.filter(review_id=rev)
            imageList = []

            for img in images:
                if img.image:
                    imageList.append(request.build_absolute_uri(img.image.url))

            data.append({
                "reviewId": rev.review_id,
                "userId": rev.user_id.user_id,

                # ✅ ADD THESE (MOST IMPORTANT)
                "userName": full_name,
                "userImage": profile_image,

                "rating": rev.rating,
                "comment": rev.comment,
                "createdAt": rev.created_at,
                "images": imageList
            })
        
        return JsonResponse({"data": data}, status=200)
 
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
# 48) ADD OR REMOVE WISHLIST
@csrf_exempt
@api_view(["POST"])
def addOrRemoveWishlist(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Please login first"}, status=401)

        userIdOrError = verifyToken(token)
        if isinstance(userIdOrError, dict):
            return JsonResponse(userIdOrError, status=401)

        userObj = user.objects.get(user_id=userIdOrError)

        productId = request.data.get("productId")
        colorId = request.data.get("colorId")
        # fix undefined coming from frontend
        if colorId in ["undefined", "", None]:
            colorId = None
        if not productId:
            return JsonResponse({"message": "productId required"}, status=400)

        productObj = product.objects.get(product_id=productId)

        colorObj = None
        if colorId in ["undefined", "", None]:
            colorId = None

        colorObj = None
        if colorId:
            colorObj = color.objects.filter(color_id=colorId).first()

        # ⭐ CHECK PRODUCT + COLOR
        existing = wishlist.objects.filter(
            user_id=userObj,
            product_id=productObj,
            color=colorObj
        ).first()

        if existing:
            existing.delete()
            return JsonResponse({"message": "removed from wishlist"}, status=200)

        wishlist.objects.create(
            user_id=userObj,
            product_id=productObj,
            color=colorObj
        )

        return JsonResponse({"message": "added to wishlist"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

#50)BANNERIMAGE API
@csrf_exempt
@api_view(['POST'])
def CreateBannerImage(request):
    try:
        Image=request.data.get("Image")
        if not Image:
            return JsonResponse({"message":"image is required!!"},status=400)
        bannerIamges.objects.create(
            image=Image
        )
        return JsonResponse({"message":"banner created !!!"},status=200)
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)

#51) GET BANNER IMAGES
@csrf_exempt
@api_view(["GET"])
def getAllBanners(request):
    try:
        banners = bannerIamges.objects.all()

        data = []
        for banner in banners:
            data.append({
                "bannerId": banner.banner_id,
                "image": request.build_absolute_uri(banner.image.url)
            })

        return JsonResponse({"data": data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        
# ------------------------------------------------------------------------------------------
# Configure Gemini
# Initialize client with API key
client = genai.Client(api_key="AIzaSyBF9fysx3HisSQR6gs72w88XODXc8Qmb60")

# ---------------- BODY TYPE CALCULATION ----------------
def calculate_body_type(bust, waist, hips):
    bust = float(bust)
    waist = float(waist)
    hips = float(hips)

    diff = abs(bust - hips)

    if diff <= 2 and waist <= bust * 0.75:
        return "hourglass"
    elif hips > bust + 2:
        return "pear"
    elif bust > hips + 2:
        return "inverted triangle"
    elif waist >= bust * 0.85:
        return "apple"
    else:
        return "rectangle"


# ---------------- AI FINAL SUGGESTION ----------------
def ai_final_suggestion(body, skin, item):    
    try:
        prompt = f"""
You are a fashion stylist.

User body type: {body}
User skin tone: {skin}
Requested clothing: {item}

If body type is "none":
- Suggest only colors
- Do NOT mention body shape
- Do NOT suggest fit styles

Otherwise:
- Suggest clothing type
- Fit style
- Suitable colors

Max 12 words. One short sentence.
"""

        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=prompt,
        )

        reply = response.text.strip()
        reply_words = reply.split()
        return " ".join(reply_words[:12])

    except:
        return "Try balanced silhouettes in colors that suit your tone."


def format_products(products):
    product_list = []

    for p in products:
        img = productImages.objects.filter(product_id=p).first()
        image_url = img.images.url if img else ""

        product_list.append({
            "id": p.product_id,
            "title": p.product_name,
            "price": str(p.price),
            "image": image_url
        })

    return product_list
# ---------------- CHATBOT VIEW ----------------
@csrf_exempt
@api_view(["POST"])
def chatbot(request):
    request.session.set_expiry(0)  # 👈 24 HOURS
    request.session.modified = True 
    try:
        message = request.data.get("message", "")

        message = re.sub(r"[^\w\s,]", "", message)

        message = message.lower().strip()

        # detect greeting BEFORE correction
        words = message.split()
        if words and words[0] in ["hi","hello","hey","hy","hii","hyy"]:
            request.session["chat_step"] = "start"
            return JsonResponse({"reply": "Hi! How can I help you today?"})

        # now apply correction
        if not re.search(r"\d", message):
            message = str(TextBlob(message).correct())

        message = message.lower().strip()
        step = request.session.get("chat_step", "start")
        # 👈 NEW: Check if user already told us their info (PERSISTENT MEMORY)
        body = request.session.get("body_type")
        skin = request.session.get("skin_tone")

        if body and skin:  # 👈 If we know user's body/skin from previous chats
            # Skip ALL questions - give direct answer!
            if any(word in message for word in ["suits", "wear", "show", "dress", "jeans", "top"]):
                item = request.session.get("requested_item", "outfits")
                ai_reply = ai_final_suggestion(body, skin, item)
                
                products = product.objects.filter(is_active=True)[:3]
                product_list = format_products(products)
                
                return JsonResponse({
                    "reply": f"For your {body} shape & {skin} tone: {ai_reply}",
                    "products": product_list,
                    "body": body,
                    "tone": skin
                })
 
        if any(word in message for word in ["thank", "thanks", "thank you"]):
            request.session["chat_step"] = "start"
            request.session.modified = True
            request.session["body_type"] = None      # 👈 ADD THIS
            request.session["skin_tone"] = None
            return JsonResponse({"reply": "You’re welcome! Let me know if you need anything else."})
 
        if any(x in message for x in ["no thanks", "no thank you", "nothing"]):
            request.session["chat_step"] = "start"
            request.session.modified = True
            request.session["body_type"] = None      # 👈 ADD THIS
            request.session["skin_tone"] = None  
            return JsonResponse({"reply": "Alright! I’m here if you need styling help."})
 
        # GREETING RESET
        words = message.split()
        if words and words[0] in ["hi","hello","hey","hy","hii","hyy"]:
            request.session["chat_step"] = "start"
            request.session["body_type"] = None      # 👈 ADD THIS
            request.session["skin_tone"] = None 
            return JsonResponse({"reply": "Hi! How can I help you today?"})
 
        # SHOW PRODUCTS AFTER SUGGESTION
        if any(word in message for word in ["show", "products", "options"]):
            body = request.session.get("body_type")
            item = request.session.get("requested_item")
 
            if  item:
                products = product.objects.filter(category__category_name__icontains=item,is_active=True)[:3]
 
                product_list = format_products(products)
                
 
                return JsonResponse({
                    "reply": "Here are some options for you.",
                    "products": product_list
                })
 
        
        # STEP 1: START
        if step == "start":

            # -------- COLOR DIRECT REQUEST --------
            colors = ["red","green","blue","black","white","yellow","pink","purple","orange","wine","olive green"]
            items = ["jeans","dress","top","shirt","trouser"]

            for color in colors:

                if color in message:

                    selected_item = None

                    for item in items:
                        if item in message:
                            selected_item = item
                            break

                    if selected_item:
                        products = product.objects.filter(
                            color__color_name__icontains=color,
                            category__category_name__icontains=selected_item,
                            is_active=True
                        )[:3]
                    else:
                        products = product.objects.filter(
                            color__color_name__icontains=color,
                            is_active=True
                        )[:3]

                    product_list = format_products(products)

                    return JsonResponse({
                        "reply": f"Here are some {color} {selected_item if selected_item else 'outfits'} for you.",
                        "products": product_list,
                        "item": selected_item,
                        "color": color
                    })


            # -------- MULTIPLE CLOTHING ITEMS --------
            

            found_items = []

            for item in items:
                if item in message or item + "s" in message:
                    found_items.append(item)

            if len(found_items) >= 2:

                main_item = found_items[-1]
                pair_item = found_items[0]

                products = product.objects.filter(
                    category__category_name__icontains=main_item,
                    is_active=True
                )[:3]

                product_list = format_products(products)

                return JsonResponse({
                    "reply": f"These {main_item}s go well with {pair_item}.",
                    "products": product_list,
                    "item": main_item
                })


            # -------- SINGLE CLOTHING ITEM --------
            for item in items:
                if item in message:
                    request.session["requested_item"] = item
                    break


            # -------- COLOR QUESTIONS --------
            if any(word in message for word in [
                "color", "colour", "colors", "colours",
                "what color", "what colour", 
                "which color", "which colour",
                "color suits", "colour suits"
            ]):

                skin = request.session.get("skin_tone")

                if skin:
                    request.session["chat_step"] = "final_suggest"
                    request.session["color_only"] = True

                    # jump directly to final suggestion
                    step = "final_suggest"

                    return JsonResponse({
                        "reply": "Let me suggest colors based on your previous skin tone."
                    })

                request.session["chat_step"] = "ask_skin"
                request.session["color_only"] = True
                request.session["skin_tone"] = None
                request.session["body_type"] = None
                request.session["requested_item"] = None
                request.session.modified = True

                return JsonResponse({
                    "reply": "What is your skin tone?"
                })


            # -------- BODY / FIT QUESTIONS --------
            if any(word in message for word in [
                "which clothes",
                "what clothes",
                "suits me",
                "suit me",
                "what should i wear"
            ]):

                body = request.session.get("body_type")
                skin = request.session.get("skin_tone")

                # If already saved → skip questions
                if body:
                    request.session["chat_step"] = "final_suggest"
                    return JsonResponse({
                        "reply": "Let me suggest something based on your previous preferences."
                    })

                request.session["chat_step"] = "ask_body_type"
                request.session["color_only"] = False
                request.session["skin_tone"] = None
                request.session.modified = True

                return JsonResponse({
                    "reply": "Do you know your body type?"
                })


            # -------- DEFAULT FALLBACK --------
            return JsonResponse({
                "reply": "I help with clothing suggestions. Ask me about outfits, colors, or styles."
            })
       
        # STEP 2: BODY TYPE
        elif step == "ask_body_type":

            valid_body_types = ["pear","apple","hourglass","rectangle","inverted triangle"]

            if "no" in message:
                request.session["chat_step"] = "ask_measurements"
                request.session.modified = True
                return JsonResponse({
                    "reply": "Tell me your bust, waist, and hip measurements (for example: 32, 24, 40)."
                })

            elif message in ["yes", "y", "yeah", "yup"]:
                return JsonResponse({
                    "reply": "Great! What is your body type? (pear, apple, hourglass, rectangle, inverted triangle)"
                })

            elif any(bt in message for bt in valid_body_types):

                for bt in valid_body_types:
                    if bt in message:
                        request.session["body_type"] = bt
                        break

                request.session["chat_step"] = "final_suggest"

                return JsonResponse({
                    "reply": "Got it! Let me suggest something for you."
                })

            else:
                return JsonResponse({
                    "reply": "Please tell me a body type: pear, apple, hourglass, rectangle, or inverted triangle."
                })
                        
        # STEP 3: MEASUREMENTS
        elif step == "ask_measurements":
            try:
                numbers = re.findall(r"\d+\.?\d*", message)
 
                if len(numbers) < 3:
                    return JsonResponse({
                        "reply": "Please enter three measurements like 32, 24, 40."
                    })
 
                bust = float(numbers[0])
                waist = float(numbers[1])
                hips = float(numbers[2])
 
                body_type = calculate_body_type(bust, waist, hips)
 
                request.session["body_type"] = body_type
                request.session["chat_step"] = "final_suggest"

                return JsonResponse({
                    "reply": f"You have a {body_type} body shape. Let me suggest outfits for you."
                })
 
            except:
                return JsonResponse({
                    "reply": "Please enter measurements like 32, 24, 40."
                })
 
        # STEP 4: SKIN TONE
        elif step == "ask_skin":
 
            if any(word in message for word in ["dont", "don't", "no", "not sure"]):
                return JsonResponse({
                    "reply": "Check wrist veins: green warm, blue or purple cool."
                })
 
            tone = None
 
            if "warm" in message or "green" in message:
                tone = "warm"
            elif "cool" in message or "blue" in message or "purple" in message:
                tone = "cool"
 
    # if tone still not detected → ask again
            if not tone:
                return JsonResponse({
                    "reply": "Please choose warm, cool, or tell me your vein color."
                })
 
            request.session["skin_tone"] = tone
            request.session["chat_step"] = "final_suggest"
 
            return JsonResponse({
                "reply": "Got it! Let me suggest something for you."
            })
        # STEP 5: FINAL ANSWER
        elif step == "final_suggest":
            body = request.session.get("body_type")
            skin = request.session.get("skin_tone")
            item = request.session.get("requested_item", "outfit")
 
            color_only = request.session.get("color_only", False)
 
            ai_item = item if item else "clothes"
 
            if color_only:
                ai_reply = ai_final_suggestion("none", skin, ai_item)
                final_reply = ai_reply
            else:
                ai_reply = ai_final_suggestion(body, skin, ai_item)

                if body:
                    final_reply = f"You have a {body} shape. {ai_reply}"
                else:
                    final_reply = ai_reply
            
 
            # fetch products from DB
            products = product.objects.filter(is_active=True)
 
# only filter by category if user asked for specific item
            if item:
                products = products.filter(
                    category__category_name__icontains=item
                )
 
            products = products[:3]
 
            product_list = format_products(products)
 
            request.session["chat_step"] = "start"
            request.session["color_only"] = False
            request.session.modified = True
 
            if color_only:
                return JsonResponse({
                    "reply": final_reply + " Here are some options for you.",
                    "products": product_list,
                    "tone": skin
                })
            else:
                return JsonResponse({
                    "reply": final_reply + " Here are some options for you.",
                    "products": product_list,
                    "body": body,
                    "item": item if item else None
                })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 

@csrf_exempt
@api_view(["POST"])
def clearChatSession(request):
    # 👈 CLEAR ALL CHAT DATA ON PAGE LOAD
    request.session["chat_step"] = "start"
    request.session["body_type"] = None
    request.session["skin_tone"] = None
    request.session["requested_item"] = None
    request.session["color_only"] = False
    request.session.modified = True
    return JsonResponse({"status": "cleared"})


# create stock   
@csrf_exempt
@api_view(["POST"])
def createStock(request):
    try:
        productId = request.data.get("productId")
        sizeId = request.data.get("sizeId")
        quantity = request.data.get("quantity")

        if not productId or not sizeId or quantity is None:
            return JsonResponse({"message":"productId, sizeId and quantity are required"},status=400)

        try:
            productObj = product.objects.get(product_id=productId)
        except product.DoesNotExist:
            return JsonResponse({"message":"Product not found"}, status=404)

        try:
            sizeObj = size.objects.get(size_name=sizeId)
        except size.DoesNotExist:
            return JsonResponse({"message":"Size not found"}, status=404)

        quantity = int(quantity)
        if quantity < 0:
            return JsonResponse({"message":"Quantity cannot be negative"},status=400)

        # Check if stock already exists
        stockObj = stock.objects.filter(
            product_id=productObj,
            size_id=sizeObj
        ).first()

        if stockObj:
            # Update stock
            stockObj.stock_quantity = quantity
            stockObj.save()
            message = "Stock updated successfully"
        else:
            # Create new stock
            stock.objects.create(
                product_id=productObj,
                size_id=sizeObj,
                stock_quantity=quantity
            )
            message = "Stock created successfully"

        return JsonResponse({"message": message}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# get stock
@csrf_exempt
@api_view(['GET'])
def getProductStock(request):
    try:
        productID = request.GET.get("productID")
        if not productID:
            return JsonResponse({"message":"productID is required"}, status=400)

        try:
            productObj = product.objects.get(product_id=productID)
        except product.DoesNotExist:
            return JsonResponse({"message":"Product not found"}, status=404)

        # Get stock data
        stockList = stock.objects.filter(product_id=productObj)

        stockData = []
        for item in stockList:
            stockData.append({
                "size": item.size_id.size_name,
                "quantity": item.stock_quantity
            })

        response = {
            "product_id": productObj.product_id,
            "product_name": productObj.product_name,
            "stock": stockData
        }

        return JsonResponse({"data":response}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  
    
#DELIVERY LOGIN 
@csrf_exempt
@api_view(['POST'])
def deliveryLogin(request):
    try:
        Email = request.data.get("Email")
        password = request.data.get("password")

        if not Email:
            return JsonResponse({"error": "Email is required"}, status=400)

        Email = Email.strip().lower()

        EmailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(EmailRegex, Email):
            return JsonResponse({"error": "invalid email format"}, status=400)

        if not password:
            return JsonResponse({"error": "Password is required"}, status=400)

        try:
            deliveryObj = deliveryPerson.objects.get(email=Email)
        except deliveryPerson.DoesNotExist:
            return JsonResponse({"error": "Delivery person not found"}, status=404)

        if not check_password(password, deliveryObj.password):
            return JsonResponse({"error": "password not matched"}, status=401)

        token = generateDeliveryToken(deliveryObj.delivery_person_id)

        return JsonResponse({
            "message": "login successfully",
            "token": token
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@api_view(["GET"])
def deliveryDashboard(request):
    try:
        #  TOKEN CHECK 
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)
        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        try:
            deliveryObj = deliveryPerson.objects.get(
                delivery_person_id=deliveryIdOrError
            )
        except deliveryPerson.DoesNotExist:
            return JsonResponse({"message": "Delivery person not found"}, status=404)

        
        #  FILTER 
        filter_type = request.GET.get("filter")

        orders = order.objects.filter(assigned_delivery_person=deliveryObj)

        if filter_type == "all":
            # MY ORDERS (NON DELIVERED)
            orders = orders.filter(status__in=[1,2,3])

        elif filter_type == "completed":
            # DELIVERED ORDERS
            orders = orders.filter(status=4)

        elif filter_type == "dashboard":
            # SAME AS MY ORDERS
            orders = orders.filter(status__in=[1,2,3])

        
        # COUNTS 
        assignedOrders = order.objects.filter(
            assigned_delivery_person=deliveryObj,
            status__in=[1, 2]
        )

        outForDeliveryOrders = order.objects.filter(
            assigned_delivery_person=deliveryObj,
            status=3
        )

        todayDate = datetime.date.today()

        deliveredTodayOrders = order.objects.filter(
            assigned_delivery_person=deliveryObj,
            status=4,
            updated_at__date=todayDate
        )

        #  ORDER LIST 
        ordersList = []

        for o in orders:
            ordersList.append({
                "orderId": o.order_id,
                "customerName": o.address_id.full_name,
                "address": f"{o.address_id.street_address}, {o.address_id.pincode.city_id.city_name}",
                "status": o.status,
                "date": o.created_at.strftime("%d-%m-%Y")
            })

        return JsonResponse({
            "deliveryPersonName": deliveryObj.delivery_person_name,
            "email": deliveryObj.email,
            "mobile": deliveryObj.mobile,

            "assignedCount": assignedOrders.count(),
            "outForDeliveryCount": outForDeliveryOrders.count(),
            "deliveredTodayCount": deliveredTodayOrders.count(),

            "orders": ordersList
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@api_view(["POST"])
def updateDeliveryProfile(request):

    try:

        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message":"Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)

        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        deliveryObj = deliveryPerson.objects.get(
            delivery_person_id = deliveryIdOrError
        )

        deliveryObj.delivery_person_name = request.data.get("name")
        deliveryObj.email = request.data.get("email")
        deliveryObj.mobile = request.data.get("mobile")

        deliveryObj.save()

        return JsonResponse({
            "message":"Profile updated successfully"
        })

    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)  

# GET UNASSIGNED ORDER
@csrf_exempt
@api_view(["GET"])
def getUnassignedOrders(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)
        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        deliveryObj = deliveryPerson.objects.get(
            delivery_person_id=deliveryIdOrError
        )

        orders = order.objects.filter(
            assigned_delivery_person__isnull=True,
            status=0,  
            address_id__pincode__city_id=deliveryObj.city
        )

        orderList = []

        for o in orders:
            orderList.append({
                "orderId": o.order_id,
                "customer": o.address_id.full_name,
                "address": o.address_id.street_address,
                "total": float(o.grand_total),
                "status": o.get_status_display()
            })

        return JsonResponse({"orders": orderList}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

#GET SINGLE ORDER 
@csrf_exempt
@api_view(["GET"])
def getSingleOrder(request, order_id):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)
        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        try:
            orderObj = order.objects.get(order_id=order_id)
        except order.DoesNotExist:
            return JsonResponse({"message": "Order not found"}, status=404)

        items = orderItems.objects.filter(order_id=orderObj)

        itemList = []
        for i in items:
            itemList.append({
                "product": i.product_id.product_name,
                "quantity": i.quantity,
                "price": float(i.price),
                "size": i.size.size_name
            })

        return JsonResponse({
            "orderId": orderObj.order_id,
            "customer": orderObj.address_id.full_name,
            "address": orderObj.address_id.street_address,
            "total": float(orderObj.grand_total),
            "items": itemList
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# accept delivery order
@csrf_exempt
@api_view(["POST"])
def acceptDeliveryOrder(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)
        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        orderId = request.data.get("orderId")
        if not orderId:
            return JsonResponse({"message": "Order ID required"}, status=400)

        try:
            orderObj = order.objects.get(order_id=orderId)
        except order.DoesNotExist:
            return JsonResponse({"message": "Order not found"}, status=404)

        deliveryObj = deliveryPerson.objects.get(
            delivery_person_id=deliveryIdOrError
        )
        

        # 1. Order must be confirmed
        if orderObj.status != 0:
            return JsonResponse({"message": "Order not available for acceptance"}, status=400)

        # 2. Order must not already be assigned
        if orderObj.assigned_delivery_person:
            return JsonResponse({"message": "Order already assigned"}, status=400)
        
        # 3. City must match
        orderCity = orderObj.address_id.pincode.city_id
        if deliveryObj.city.city_id != orderCity.city_id:
            return JsonResponse({"message": "You are not allowed to accept this order (Different city)"}, status=403)

        #  ACCEPT ORDER 
        orderObj.assigned_delivery_person = deliveryObj
        orderObj.status = 2  
        orderObj.save()

        orderHistory.objects.create(
            order_id=orderObj,
            user_id=orderObj.user_id,
            address_id=orderObj.address_id,
            delivery_person_id=deliveryObj,
            message="Order accepted"
        )

        return JsonResponse({"message": "Order accepted successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# out for delivery
@csrf_exempt
@api_view(["POST"])
def markOutForDelivery(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)
        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        orderId = request.data.get("orderId")
        orderObj = order.objects.get(order_id=orderId)

        orderObj.status = 3  
        orderObj.save()

        orderHistory.objects.create(
            order_id=orderObj,
            user_id=orderObj.user_id,
            address_id=orderObj.address_id,
            delivery_person_id=orderObj.assigned_delivery_person,
            message="Order marked Out for Delivery"
        )

        return JsonResponse({"message": "Marked Out for Delivery"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# complete delivery
@csrf_exempt
@api_view(["POST"])
def completeDelivery(request):
    try:
        token = request.headers.get("token")
        if not token:
            return JsonResponse({"message": "Login required"}, status=401)

        deliveryIdOrError = verifyDeliveryToken(token)
        if isinstance(deliveryIdOrError, dict):
            return JsonResponse(deliveryIdOrError, status=401)

        orderId = request.data.get("orderId")

        orderObj = order.objects.get(order_id=orderId)

        orderObj.status = 4  # Delivered
        orderObj.save()

        orderHistory.objects.create(
            order_id=orderObj,
            user_id=orderObj.user_id,
            address_id=orderObj.address_id,
            delivery_person_id=orderObj.assigned_delivery_person,
            message="Order delivered successfully"
        )

        return JsonResponse({"message": "Delivery completed"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def deliveryOrderDetail(request, order_id):
    return render(request, "delivery_order_detail.html", {"order_id": order_id})

def contact(request):

    if request.method == "POST":
        email = request.POST.get("email")
        msg = request.POST.get("msg")

        message = f"""
        New Message From KASHA 

        From: {email}

        Message:
        {msg}
        """

        send_mail(
            "New Message From KASHA",
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

    return render(request, "contact.html")

