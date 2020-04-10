# Folder Structure
When a Django project is created by running 
```
django-admin startproject projectname
```
It creates the following files
```
projectname
├── manage.py
└── projectname
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Each django project is made of multiple apps created using 
```
django-admin startapp appname
```

Our meeting-scheduler app consists of three apps meetings, users and scheduler.

## How Django apps work
When user request an address or opens a link, Django tries to find an matching url pattern in `urls.py` file. Each pattern in the `urls.py` file will specify a function to execute when the pattern is matched. The function returns the HTML to be rendered by the client browser. Usually the HTML file is an template which will display the data provided by the view function as context data.

## `urls.py`
This file determines what happens when user opens an address (routes).  
The project folder (meeting_scheduler) contains a `urls.py`.
An example content of the file is:
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduler.urls')),
    path('user/', include('users.urls')),
    path('meeting/', include('meetings.urls'))

]
```
this means when the user opens `http://localhost:port/admin/` the function admin.site.urls is executed. Our each app (scheduler, users, meetings) has its on `urls.py`. These files are specified in the following lines.  
Url patterns used in the project  
`/`: home page  
`user/register`: To create new user  
`user/login`: For existing users to log in  
The following addresses are only accessible if the user is logged in  
`user/edit`: To edit user profile  
`user/logout`: To logout  
`user/profile`: To view user profile  
`meeting`: To view the meetings user is attending  
`meeting/notifications`: To read all the notifications  
`meeting/create`: To create a meeting  
The following addresses require an integer variable to identify a specific meeting
`meeting/<mid>/`: To see the details of a meeting  
`meeting/<mid>/invite`: To see the invite form of a meeting  
`meeting/<mid>/message`: To message about a meeting  
`meeting/<mid>/edit`: To edit a meeting  
`meeting/<mid>/delete`: To delete a meeting  
`meeting/<mid>/accept`: To accept invitation to a meeting  
`meeting/<mid>/decline`: To decline invitation to a meeting  



## `views.py`
Each app has its own `views.py`. Views take the HTTP requests and returns a HTTPResponse. Views can be defined in two ways in Django
* Class based views  
These classes inherits base view classes defined in django  
* Function based views  
These functions take request as an argument and returns HTTPResponse

For example:  
In meetings/urls.py
```
    path('create/', MeetingCreate.as_view(), name='create_view'),
```
MeetingCreate is a class defined in meetings/views.py. When someone opens `http://localhost:port/meeting/create`, the base class of MeetingCreate has an as_view() method that returns a response.

In users/urls.py
```
path('login/', views.user_login, name='login_view')
```
Hence when someone opens `http://localhost:port/user/create` it executes user_login function in the users/views.py

## templates
Templates are files defined in templates folder. They use Jinja2 to run python code inside HTML. 

## static
These are the static files in the project including the stylesheets and scripts.