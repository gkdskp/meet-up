from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login_view'),
	path('register/', views.register, name='register_view'),
	path('profile/', views.profile, name='profile_view'),
	path('logout/', views.user_logout, name='logout_view'),
	path('edit/', views.profile_edit, name='profile_edit_view')
]
