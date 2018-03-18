from django import forms
from django.contrib.auth.models import User
from studeals.models import UserProfile
from studeals.auth import recaptcha_check

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text="Re-enter your password for confirmation.")
	email = forms.CharField(widget=forms.EmailInput(), help_text="Use your institution email address ending with <b>ac.uk</b>.")

	class Meta:
		model = User
		fields = ('username','email','password')

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		email = cleaned_data.get('email')
		recaptcha_response = self.data['g-recaptcha-response']

		if password != confirm_password:
			self.add_error('confirm_password', "The entered passwords do not match.")

		if not email.endswith('ac.uk'):
			self.add_error('email', 'The email address provided is not an educational one.')

		try:
			User.objects.get(email=email)
			self.add_error('email', 'There is already an account registered with this email address.')
		except User.DoesNotExist:
			pass

		if not (recaptcha_response and recaptcha_check(recaptcha_response)):
			self.add_error(None, 'The CAPTCHA validation failed, please try again.')

		return cleaned_data

class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=('picture',)

class PasswordResetForm(forms.ModelForm):
	email = forms.CharField(widget=forms.EmailInput(), help_text="Enter your account's email address.")
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text="Re-enter your password for confirmation.")

	class Meta:
		model = User
		fields=('email','password')

	def clean(self):
		cleaned_data = super(PasswordResetForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		email = cleaned_data.get('email')
		recaptcha_response = self.data['g-recaptcha-response']

		if password != confirm_password:
			self.add_error('confirm_password', "The entered passwords do not match.")

		if self.instance.email != email:
			self.add_error('email', 'The entered email address does not correspond with the one in the system.')

		if not (recaptcha_response and recaptcha_check(recaptcha_response)):
			self.add_error(None, 'The CAPTCHA validation failed, please try again.')

		return cleaned_data

class PasswordResetRequestForm(forms.Form):
	email = forms.CharField(widget=forms.EmailInput(), help_text="Enter your account's email address.")

	def clean(self):
		cleaned_data = super(PasswordResetRequestFOrm, self).clean()
		recaptcha_response = self.data['g-recaptcha-response']

		if not (recaptcha_response and recaptcha_check(recaptcha_response)):
			self.add_error(None, 'The CAPTCHA validation failed, please try again.')

		return cleaned_data
