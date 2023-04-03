from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required



def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form })


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:login")


def profile_request(request):
    if request.user.is_authenticated:
        user = request.user
        users = User.objects.filter(is_active=True)
        print(request)
        context = {
                      "user": user,
                      "users": users,
        }
        return render(request, "main/profile.html", context)
    else:
        return redirect("main:login")


def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        if request.FILES.get('profile_image'):
            photo = request.FILES['profile_image']
            user.profile_image = photo
            fs = FileSystemStorage()
            filename = fs.save( user.profile_image, photo)
            uploaded_photo_url = fs.url(filename)
            return uploaded_photo_url
        user.save()
        messages.success(request, "Profile updated successfully!")

         # ndryshimi i fjalëkalimit
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully!")
        else:
            for error in password_form.errors.values():
                messages.error(request, error)

        return redirect('main:profile')
    else:
        user = request.user
        context = {
            'user': user,
            'password_form': PasswordChangeForm(request.user),
        }
        return render(request, 'main/edit_profile.html', context)




#def edit_profile(request):
#    if request.method == "POST":
#        user = request.user
#       if request.FILES.get('profile_image'):
#            photo = request.FILES['profile_image']
#            user.profile_image = photo
#            fs = FileSystemStorage()
#            filename = fs.save( user.profile_image, photo)
#            uploaded_photo_url = fs.url(filename)
#            return uploaded_photo_url
#        user.save()
#        messages.success(request, "Profile updated successfully!")

        # ndryshimi i fjalëkalimit
#        password_form = PasswordChangeForm(request.user, request.POST)
#        if password_form.is_valid():
#            user = password_form.save()
#            update_session_auth_hash(request, user)
#            messages.success(request, "Password updated successfully!")
#        else:
#            for error in password_form.errors.values():
#                messages.error(request, error)

#        return redirect('main:profile')
#    else:
#        user = request.user
#        context = {
#            'user': user,
#            'password_form': PasswordChangeForm(request.user),
#        }
#        return render(request, 'main/edit_profile.html', context)

