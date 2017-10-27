# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, backends, logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User

# readies and renders the register and login page
def index(request):
    return render(request, "logreg/logreg.html")
# validates a new users information and creates that user
def register(request):
    if request.method == "POST":
            user = User.objects.create_user(username=request.POST["email"], email=request.POST["email"], password=request.POST["password"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect("/shop")
# verifies the users login infromation and adds their information to session
def log_in(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    # Redirect to a success page.
        return redirect("/shop")
    else:
        return redirect("/")
# removes the current users infromation from session and logs them out
def log_out(request):
    logout(request)
    return redirect("/")

@login_required
def home(request):
    return render(request, '../commerce_app/index.html')

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'logreg/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'logreg/password.html', {'form': form})