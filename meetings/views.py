from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Meeting, MeetingAction
from users.models import User
from .forms import MeetingUpdateForm, MeetingInviteForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.db.models import Q
from operator import attrgetter


class MeetingsListView(ListView):
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super(MeetingsListView, self).get_context_data(**kwargs)

        accepted_meetings = set()
        try:
            for meeting in Meeting.objects.filter(creator=self.request.user, status=True):
                accepted_meetings.add(meeting)
            for meeting in MeetingAction.objects.filter(sender=self.request.user, action=2):
                if(meeting.meeting.status):
                    accepted_meetings.add(meeting.meeting)

            context['meetings'] = sorted(
                accepted_meetings, key=attrgetter('start_time'))
        except:
            pass
        return context


class NotificationListView(ListView):
    model = Meeting
    template_name = 'meetings/meetingaction_list.html'

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        try:
            context['active_notifications'] = MeetingAction.objects.filter(Q(reciever=self.request.user) & Q(
                decision_time__gte=self.request.user.profile.last_notif_check)).order_by('-decision_time')
        except:
            context['active_notifications'] = None

        try:
            context['seen_notifications'] = MeetingAction.objects.filter(Q(reciever=self.request.user) & Q(
                 decision_time__lt=self.request.user.profile.last_notif_check)).order_by('-decision_time')
        except:
            context['seen_notifications'] = None
        
        self.request.user.profile.save()
        return context


class MeetingDetailView(DetailView):
    model = Meeting
    context_object_name = 'meeting'

    def get_context_data(self, **kwargs):
        context = super(MeetingDetailView, self).get_context_data(**kwargs)
        meeting = self.get_object()
        
        try:
            meetingaction = MeetingAction.objects.filter(Q(meeting=meeting) & (
                Q(reciever=self.request.user) | Q(sender=self.request.user)) & ~Q(action=4)).latest('decision_time')
        except MeetingAction.DoesNotExist:
            meetingaction = None

        try:
            context['participants'] = MeetingAction.objects.filter(meeting=meeting, action=2)
        except MeetingAction.DoesNotExist:
            pass
        
        try:
            context['invites'] = MeetingAction.objects.filter(meeting=meeting, action=1)
        except MeetingAction.DoesNotExist:
            pass
            
        try:
            context['declines'] = MeetingAction.objects.filter(meeting=meeting, action=3)
        except MeetingAction.DoesNotExist:
            pass

        if meeting.creator == self.request.user:
            context['perm_level'] = 0
        elif meetingaction:
            context['perm_level'] = meetingaction.action

        return context


class MeetingCreate(CreateView):
    model = Meeting
    form_class = MeetingUpdateForm

    def get_initial(self, *args, **kwargs):
        initial = super(MeetingCreate, self).get_initial(*args, **kwargs)
        initial['location'] = self.request.user.profile.location
        initial['city'] = self.request.user.profile.city
        return initial

    def form_valid(self, form):
        self.meeting = form.save(commit=False)
        self.meeting.creator = self.request.user
        self.meeting.save()
        messages.success(self.request, "Meeting created")
        return redirect('meeting_view', pk=self.meeting.pk)


class MeetingUpdate(UpdateView):
    model = Meeting
    form_class = MeetingUpdateForm

    def form_valid(self, form):
        self.meeting = form.save(commit=False)
        self.meeting.last_edit_time = timezone.now()
        self.meeting.save()

        messages.success(self.request, "Meeting updated")
        return redirect('meeting_view', pk=self.meeting.pk)


class MeetingDelete(DeleteView):
    model = Meeting
    success_url = reverse_lazy('meetings_view')
    context_object_name = 'meeting'


class MeetingInvite(FormView):
    form_class = MeetingInviteForm
    template_name = 'meetings/meeting_invite.html'

    def form_valid(self, form):
        userslist = self.request.POST.get('users').split(',')
        meetingaction = form.save(commit=False)

        meetingaction.meeting = Meeting.objects.get(mid=self.kwargs['mid'])
        meetingaction.action = 1
        meetingaction.sender = self.request.user

        for user in userslist:
            meetingaction.pk = None
            try:
                meetingaction.reciever = User.objects.get(username=user)
                meetingaction.save()
            except:
                continue

        return redirect('meeting_view', pk=self.kwargs['mid'])

    def get_context_data(self, *args, **kwargs):
        context = super(MeetingInvite, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class MeetingMessage(FormView):
    form_class = MeetingInviteForm
    template_name = 'meetings/meeting_message.html'

    def form_valid(self, form):
        meetingaction = form.save(commit=False)
        meetingaction.action = 4
        meetingaction.meeting = Meeting.objects.get(mid=self.kwargs['mid'])
        meetingaction.reciever = meetingaction.meeting.creator
        meetingaction.sender = self.request.user
        meetingaction.save()

        return redirect('meeting_view', pk=self.kwargs['mid'])

def accept_invite(request, mid):
    meetingaction = MeetingAction.objects.filter(
        meeting=mid, reciever=request.user).latest('decision_time')
    if(meetingaction.action == 1):
        meetingaction.reciever, meetingaction.sender = meetingaction.sender, meetingaction.reciever
        meetingaction.action = 2
        meetingaction.save()

        return redirect('meeting_view', pk=mid)


def decline_invite(request, mid):
    meetingaction = MeetingAction.objects.filter(Q(meeting=mid) & (
        Q(reciever=request.user) | Q(sender=request.user))).latest('decision_time')
    if(meetingaction.action == 1 or meetingaction.action == 2):
        if(meetingaction.action == 1):
            meetingaction.sender, meetingaction.reciever = meetingaction.reciever, meetingaction.sender
        meetingaction.action = 3
        meetingaction.save()

        return redirect('meeting_view', pk=mid)


def cancel_invite(request, mid, username):
    user = User.objects.get(username=username)
    MeetingAction.objects.get(meeting=mid, reciever=user, action=1).delete()
    return redirect('meeting_view', pk=mid) 