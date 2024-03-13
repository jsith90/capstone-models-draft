from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, UserUpdateForm, PasswordUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def login_user(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("Welcome back!"))
			return redirect('index')
		else:
			messages.success(request, ("There was an error logging in, try again..."))
			return redirect('login_user')
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You were logged out!"))
	return redirect('index')

def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration successful!"))
			return redirect('index')
	else:
		form = RegisterUserForm()
	return render(request, 'authenticate/register_user.html', {
		'form':form,
		})

@login_required
def details_update(request, id):
	user = User.objects.get(pk=id)
	if request.user == user:
		if request.method == 'POST':
			form = UserUpdateForm(request.POST, instance=user)
			if form.is_valid():
				form.save()
				messages.success(request, "User details updated successfully.")
				return redirect('user_panel')
		else:
			form = UserUpdateForm(instance=user)
		return render(request, 'authenticate/details_update.html', {'form': form})
	else:
		return render(request, 'booking/index.html')

def password_update(request):
	if request.method == 'POST':
		form = PasswordUpdateForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, "Password successfully updated!")
			return redirect('user_panel')
	else:
		form = PasswordUpdateForm(request.user)
	return render(request, 'authenticate/password_update.html', {'form': form})