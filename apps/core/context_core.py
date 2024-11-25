from .models import Notification


def notification_context(request):
    notifications = Notification.objects.all()
    return {'notifications': notifications}