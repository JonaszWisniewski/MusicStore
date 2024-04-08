from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SignUpForm, UserUpdateForm, ProfileUpdateForm, PasswordForm
from .models import Profile
from django.contrib import messages

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # sends all information from the form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save() # saves into the database if the form is valid
            messages.success(request, f'Successfully created an account for {username}')
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, user)
            age = form.cleaned_data.get('age')
            country =form.cleaned_data.get('country')
            Profile.objects.create(user=user, age=age, country=country)


            return redirect('store:index')
    else:
        form = SignUpForm() # use empty form if its not post

    
    context = {'form': form}
    return render(request, 'users/signup.html', context)

def loginview(request):

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            if user is not None:
                login(request, user)
                messages.success(request, f'Successfully logged in as {username}')

                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('store:index')

            
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, f'Successfully logged out')
    return redirect('/')


@login_required
def profile(request):
    if request.method == 'POST':
        POST = request.POST.copy() # creating a copy of the request
        POST['username'] = request.user.username # accessing the username field of POST so that the current username can be grabbed and used when posting the information into userForm
        userForm = UserUpdateForm(POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, f'Your account information has been successfully updated!')
            return redirect('users:profile')
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)

    context = {"userForm": userForm, "profileForm": profileForm}

    return render(request, 'users/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:

        form = PasswordForm(user=request.user)
    return render(request, 'users/changepassword.html', {'form': form})


    
