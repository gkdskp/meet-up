from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ProfileEditForm, UserEditForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages

def user_login(request):
	if request.user.is_authenticated:
		return redirect('home_view')
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		username = request.POST.get('username')
		raw_password = request.POST.get('password')
		user = authenticate(username=request.POST.get('username'), password=raw_password)
		if user is not None:
			login(request, user)
			return redirect('home_view')
		else:
			messages.add_message(request, messages.ERROR, 'Username and password does not match')
	else:
		form = AuthenticationForm()
	return render(request, 'users/login.html', {'form': form})

def user_logout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('home_view')
	else:
		raise PermissionDenied(request)


def register(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = SignUpForm(request.POST)
			if form.is_valid():
				user = form.save()
				user.refresh_from_db()
				user.profile.location = request.POST.get('location')
				user.profile.city = request.POST.get('city')
				user.save()

				raw_password = request.POST.get('password1')
				user = authenticate(username=user.username, password=raw_password)
				login(request, user)
				return redirect('home_view')
		else:
			form = SignUpForm()
		return render(request, 'users/register.html', {'form': form})
	else:
		raise PermissionDenied(request)

def profile(request):
	return render(request, 'users/profile.html')

def profile_edit(request):
	if request.method == 'POST':
		u_form = UserEditForm(request.POST, instance=request.user)
		p_form = ProfileEditForm(request.POST, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Profile updated')
			return redirect('profile_view')
	else:
		u_form = UserEditForm(instance=request.user)
		p_form = ProfileEditForm(instance=request.user.profile)
	return render(request, 'users/edit.html', {'u_form': u_form, 'p_form': p_form})
