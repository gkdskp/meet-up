from django.db import models
from users.models import User
from django.utils import timezone


class Meeting(models.Model):
	mid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50, blank=False)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank=False)
	create_time = models.DateTimeField(auto_now_add=True)
	last_edit_time = models.DateTimeField(auto_now=True)
	desc = models.TextField(max_length=500, blank=False)
	location = models.TextField(max_length=500, blank=False)
	city = models.CharField(max_length=50, blank=False)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	status = models.BooleanField(default=True)

	def __str__(self):
		return f'{self.mid} - {self.title}'

	def delete(self, *args, **kwargs):
		self.status = False
		self.save()
		meetingaction = MeetingAction.objects.create()
		meetingaction.meeting = self
		meetingaction.action = 5
		meetingaction.sender = self.creator
		for accepted in MeetingAction.objects.filter(meeting=self,
													 action=2):
			meetingaction.pk = None
			meetingaction.reciever = accepted.sender
			meetingaction.save()


ACTION_CHOICES = [
	(1, 'invited you to attend'),
	(2, 'has accepted your invite to'),
	(3, 'cannot attend'),
	(4, 'sent you a personal message regarding '),
	(5, 'cancelled the event')
]


class MeetingAction(models.Model):
	meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True)
	sender = models.ForeignKey(
		User, on_delete=models.CASCADE, null=True, related_name='sender')
	reciever = models.ForeignKey(
		User, on_delete=models.CASCADE, null=True, related_name='reciever')
	action = models.SmallIntegerField(null=True, choices=ACTION_CHOICES)
	message = models.TextField(max_length=500, blank=False)
	decision_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'o' or ''
