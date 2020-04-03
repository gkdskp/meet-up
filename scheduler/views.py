from django.shortcuts import render, redirect
from meetings import views as meetings_views

def home(request):
	if request.user.is_authenticated:
		return redirect('meetings_view')
	else:
		return render(request, template_name='scheduler/home.html')