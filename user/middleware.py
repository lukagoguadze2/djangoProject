from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout
from django.conf import settings
from .models import User


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_profile = request.user
                # თუ ბოლო აქტივობიდან გასულია (settings.USER_IDLE_ALLOWED_TIME) წამი დავალოგაუთოთ
                if timezone.now() - user_profile.last_activity > timedelta(seconds=settings.USER_IDLE_ALLOWED_TIME):
                    logout(request)
                else:
                    user_profile.last_activity = timezone.now()
                    user_profile.save()
            except User.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
