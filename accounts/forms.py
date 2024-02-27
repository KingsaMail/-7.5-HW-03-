from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        users_ = Group.objects.get(name="users_")
        user.groups.add(users_)
        return user