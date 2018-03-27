from django import forms
from django.db import models
from django.contrib.auth.models import User
from studeals.models import UserProfile, Offer, Category
from studeals.auth import recaptcha_check
from django.utils.timezone import now
from datetime import datetime
class UserForm(forms.ModelForm):
    """
    Form for user registration
    """
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Re-enter your password for confirmation."
    )
    email = forms.CharField(
        widget=forms.EmailInput(),
        help_text="Use your institution email address ending with <b>ac.uk</b>."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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
            self.add_error(
                'email',
                'There is already an account registered with this email address.'
            )
        except User.DoesNotExist:
            pass

        if not (recaptcha_response and recaptcha_check(recaptcha_response)):
            self.add_error(None, 'The CAPTCHA validation failed, please try again.')

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    """
    Form for user profile editing
    """
    class Meta:
        model = UserProfile
        fields = ('picture',)

class PasswordResetForm(forms.ModelForm):
    """
    Form for password reset
    """
    email = forms.CharField(
        widget=forms.EmailInput(),
        help_text="Enter your account's email address."
    )
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Re-enter your password for confirmation."
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        recaptcha_response = self.data['g-recaptcha-response']

        if password != confirm_password:
            self.add_error('confirm_password', "The entered passwords do not match.")

        if self.instance.email != email:
            self.add_error(
                'email',
                'The entered email address does not correspond with the one in the system.'
            )

        if not (recaptcha_response and recaptcha_check(recaptcha_response)):
            self.add_error(None, 'The CAPTCHA validation failed, please try again.')

        return cleaned_data

class PasswordResetRequestForm(forms.Form):
    """
    Form to request the password reset
    """
    email = forms.CharField(
        widget=forms.EmailInput(),
        help_text="Enter your account's email address."
    )

    def clean(self):
        cleaned_data = super(PasswordResetRequestForm, self).clean()
        recaptcha_response = self.data['g-recaptcha-response']

        if not (recaptcha_response and recaptcha_check(recaptcha_response)):
            self.add_error(None, 'The CAPTCHA validation failed, please try again.')

        return cleaned_data

class PasswordUpdateForm(forms.Form):
    """
    Form to update an user password
    """
    your_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(PasswordUpdateForm, self).clean()
        password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_new_password')

        if password != confirm_password:
            self.add_error('confirm_new_password', "The entered passwords do not match.")

        return cleaned_data

class OfferForm(forms.ModelForm):
    """
    Form to insert an offer
    """
    category = forms.ModelChoiceField(queryset=Category.objects.all().values_list('id','name'), initial="----")
    title = forms.CharField(max_length=20)
    slug=forms.CharField( required=False, initial="")
    price = forms.CharField(max_length=10)
    description = forms.CharField(max_length=200)
    place_address = forms.CharField(max_length=200)
    place_name = forms.CharField(max_length=50)
    picture = forms.ImageField(required=False)
    expiration_date = forms.CharField(max_length=20)

    class Meta:
        model = Offer
        exclude = ('category',)

class ContactUsForm(forms.Form):
    """
    Contact form
    """
    your_name = forms.CharField()
    your_email_address = forms.EmailField(help_text="The email address we will answer you at.")
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))

    def clean(self):
        cleaned_data = super(ContactUsForm, self).clean()
        recaptcha_response = self.data['g-recaptcha-response']

        if not (recaptcha_response and recaptcha_check(recaptcha_response)):
            self.add_error(None, 'The CAPTCHA validation failed, please try again.')

        return cleaned_data
