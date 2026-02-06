from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150, label='First name', required=True)
    last_name = forms.CharField(max_length=150, label='Last name', required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        # keep default behavior for activation via email verification
        user.save()
        return user
