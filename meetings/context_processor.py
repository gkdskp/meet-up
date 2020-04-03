from meetings.models import MeetingAction
from django.db.models import Q

def notif_count(request):
    try:
        notif_count = MeetingAction.objects.filter(Q(reciever=request.user) & Q(decision_time__gte=request.user.profile.last_notif_check)).count()
    except:
        notif_count = None
    return {
        'notif_count': notif_count
    }