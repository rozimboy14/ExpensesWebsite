from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from urllib import request

from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation.trans_null import activate
from django.views import View
import json
from django.contrib.auth.models import User
from django.contrib import messages, auth
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from .utils import token_generator
from django.utils.encoding import force_bytes,force_str


# Create your views here.


class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        usrname = data["username"]
        if not str(usrname).isalnum():
            return JsonResponse(
                {
                    "username_error": "Username should  only contain alphanumeric characters!"
                },
                status=400,
            )
        if User.objects.filter(username=usrname).exists():
            return JsonResponse(
                {
                    "username_error": "Bu Username mavjud iltimoz boshqa username kiriting"
                },
                status=409,
            )
        return JsonResponse({"username_valid": True}, status=200)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {"email_error": "email should  only contain alphanumeric characters!"},
                status=400,
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "Bu emaildan avval ro'yxatdan o'tilgan"}, status=409
            )
        return JsonResponse({"email_valid": True}, status=200)


class RegisterView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # GET USER DATA
        # Validate
        # CREATE A USER ACCOUNT
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        context = {"fieldValue": request.POST}
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=username).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short. ")
                    return render(request, "authentication/register.html", context)
                user = User.objects.create_user(username, email, password)
                user.is_active =False
                user.save()

                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64' : uidb64, 'token' : token_generator.make_token(user)})
                email_subject = "Activata your account"
                activate_url = 'http://'+domain + link
                email_body = "Hi "+user.username + \
                    'Iltimos accountni activ qilish uchun shu linkga kiring'+activate_url
                from_email = "ruzimbaimatyokubov@yandex.ru"
                email = EmailMessage(email_subject, email_body, from_email,[email])
                email.send(fail_silently=False)

                messages.success(request, "Account created successfully")
                return render(request, "authentication/register.html")

        return render(request, "authentication/register.html")

class VerificationView(View):
    def get(self, request,uidb64, token):

        try:
          id=force_str(urlsafe_base64_decode(uidb64))
          user=User.objects.get(pk=id)
          if not token_generator.check_token(user, token):
              return redirect("login"+'?mesage'+'User already activated')

          if user.is_active:
              return redirect('login')
          user.is_active = True
          user.save()
          messages.success(request, "Your account has been activated")
          return redirect('login')

        except Exception as ex:
            pass
        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")
    def post(self,request):
        username = request.POST["username"]
        password = request.POST["password"]
        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                     auth.login(request,user)
                     messages.success(request, "Xush kelibsiz " + user.username)
                     return redirect('expenses')
                messages.error(request, "Sizning accountingiz activ emailga yuborilgan link bilan activlashtiring")
                return render(request, "authentication/login.html")


            messages.error(request, "Invalid username or password")
            return render(request, "authentication/login.html")

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("login")

class RequestPasswordResetView(View):
    def get(self, request):
        return render(request,'authentication/reset-password.html')
    def post(self,request):
        email = request.POST["email"]
        context={
            "values":request.POST,
        }
        if not validate_email(email):
            messages.error(request, "Email should  only contain alphanumeric characters!")
            return render(request, 'authentication/reset-password.html')

        domain = get_current_site(request).domain
        user = User.objects.filter(email=email).first()

        if user:
           email_contents = {
                    "user":user,
                    "domain":get_current_site(request).domain,
                    "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                    "token":PasswordResetTokenGenerator().make_token(user),

                }
           link = reverse('reset-user-password',
                          kwargs={'uidb64': email_contents['uid'], 'token': email_contents['token']})


           email_subject = "Password reset Instructions"
           reset_url = f"http://{domain}{link}"
           email_message = "Hi " + user.username + \
                         'Iltimos accountni activ qilish uchun shu linkga kiring' + reset_url
           from_email = "ruzimbaimatyokubov@yandex.ru"
           email = EmailMessage(email_subject, email_message, from_email, [email])
           email.send(fail_silently=False)
           messages.success(request, "Sizning emailingizga parolni qayta tiklash uchun link yuborildi")
           return render(request, "authentication/reset-password.html")


class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token':token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.success(request, "Parolni qayta tiklash linkida xatolik iltimos qaytadan urinib koring")
            return render(request, "authentication/reset-password.html")
        except Exception as e:
            pass

        return render(request,'authentication/set-new-password.html',context)
    def post(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password != password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'authentication/set-new-password.html',context)
        if len(password) < 6:
            messages.error(request, "Password too short. ")
            return render(request, 'authentication/set-new-password.html',context)
        try:
            user_id =force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Parolni qayta tiklandi")
            return redirect('login')
        except Exception as e:
            pass
            messages.info(request, f"Something went wrong {str(e)}")
            return render(request,'authentication/set-new-password.html',context)




