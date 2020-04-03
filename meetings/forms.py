from django import forms
from .models import Meeting, MeetingAction

class MeetingUpdateForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('title', 'desc', 'start_time', 'end_time', 'location', 'city')


class MeetingInviteForm(forms.ModelForm):
    class Meta:
        model = MeetingAction
        fields = ('message',)