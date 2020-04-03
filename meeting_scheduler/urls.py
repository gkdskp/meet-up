from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduler.urls')),
    path('user/', include('users.urls')),
    path('meeting/', include('meetings.urls'))

]
