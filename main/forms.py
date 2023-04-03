from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils import timezone

# Create your forms here.
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	profile_picture = forms.ImageField(required=False)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "profile_picture")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.last_login = timezone.now()
		if self.cleaned_data['profile_image']:
			user.profile_image = self.cleaned_data['profile_image']
		if commit:
			user.save()
		return user