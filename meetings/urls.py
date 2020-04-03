from django.urls import path
from django.conf.urls import url
from . import views
from .views import MeetingsListView, MeetingDetailView, MeetingCreate, MeetingUpdate, MeetingDelete, MeetingInvite, NotificationListView, MeetingMessage

urlpatterns = [
    path('', MeetingsListView.as_view(), name='meetings_view'),
    path('notifications/', NotificationListView.as_view(), name='notifications_view'),
    path('create/', MeetingCreate.as_view(), name='create_view'),
    path('<int:pk>/', MeetingDetailView.as_view(), name='meeting_view'),
    path('<int:mid>/invite/', MeetingInvite.as_view(), name='invite_view'),
    path('<int:mid>/message/', MeetingMessage.as_view(), name='message_view'),
    path('<int:pk>/edit/', MeetingUpdate.as_view(), name='meeting_update_view'),
    path('<int:pk>/delete/', MeetingDelete.as_view(), name='meeting_delete_view'),
    path('<int:mid>/cancel/<username>/', views.cancel_invite, name='cancel_invite'),
    path('<int:mid>/accept/', views.accept_invite, name='accept_invite'),
    path('<int:mid>/decline/', views.decline_invite, name='decline_invite'),
]
