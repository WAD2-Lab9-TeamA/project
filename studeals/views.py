from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from app import settings
from datetime import datetime
from studeals.models import Category, Offer, UserProfile
from studeals.forms import UserForm, UserProfileForm, PasswordResetForm, PasswordResetRequestForm, OfferForm
from studeals.auth import activate, authenticate, tokens, send_password_reset_email, recaptcha_check
from studeals.auth.decorators import guest

def index(request):

	offers_list=Offer.objects.order_by('expiration_date')[:5]
	category_list=Category.objects.all()
	context_dict={'offers':offers_list, 'categories':category_list}
	return render(request,'studeals/index.html',context=context_dict)

def categories(request):
	category_list=Category.objects.all()
	offers_list=Offer.objects.order_by('date_added')[:1]
	context_dict={'categories':category_list,'offers': offers_list}
	
	return render(request,'studeals/categories.html',context=context_dict)

def show_category(request, category_name_slug):
	
	context_dict={}
	
	try:
		category=Category.objects.get(slug=category_name_slug)
		offers=Offer.objects.filter(category=category)

		context_dict['offers']=offers
		context_dict['category']=category

	except Category.DoesNotExist:
		context_dict['category']=None
		context_dict['offers']=None
	
	return render(request, 'studeals/category.html', context_dict)
def show_offer(request, offer_title_slug):
	
	context_dict={}
	
	try:
		offer=Offer.objects.get(slug=offer_title_slug)
		context_dict['offer']=offer
		
	except Offer.DoesNotExist:
		context_dict['offer']=None
	return render(request, 'studeals/offer.html', context_dict)
def add_offer(request, category_name_slug):
	try:
		category=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category=None

	form=OfferForm()
	if request.method=='POST':
		form=OfferForm(request.POST)
		if form.is_valid():
			if category:
				offer=form.save(commit=False)
				offer.category=Category.objects.get(slug=category_name_slug)
				offer.title=form.title
				offer.price=price
				offer.description = form.description 
				offer.place_address = form.place_address
				offer.place_name = place_name
				offer.picture = forms.ImageField(upload_to='offers', blank=True)
				offer.expiration_date = expiration_date
				offer.date_added=forms.DateField(default=datetime.now)
				offer.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	else:
		form=OfferForm()
	context_dict={'form':form, 'category':category}
	return render(request, 'studeals/add_offer.html', context_dict)
@guest
def register(request):
	if request.method == 'POST':
		form = UserForm(data=request.POST)

		if form.is_valid():
			user = form.save()

			user.set_password(user.password)
			user.is_active = False
			user.save()

			activate.send_email(request, user)

			messages.success(request, 'Thank you for signing up! To complete your registration you need to confirm your email address. We have just sent you an email containing an activation link!')
			return HttpResponseRedirect(reverse('login'))
		else:
			print(form.errors)
	else:
		form = UserForm()

	return render(request, 'studeals/register.html', {'form': form, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})

@guest
def activate_user(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None:
		if tokens.activation.check_token(user, token):
			user.is_active = True
			user.save()
			messages.success(request, 'Your account has been activated successfully! You can login now!')
		elif not user.is_active and user.last_login is None:
			activate.send_email(request, user)
			messages.warning(request, 'The activation link used has expired. A new one has been sent to your email address.')

	raise Http404("Invalid user activation token")

@guest
def request_password_reset(request):
	if request.method == 'POST':
		form = PasswordResetRequestForm(data=request.POST)

		if form.is_valid():
			try:
				user = User.objects.get(email=form.cleaned_data['email'])
				send_password_reset_email(user)
				messages.success(request, 'We have just sent you an email containing a password reset link! Check your inbox!')
				return HttpResponseRedirect(reverse('login'))
			except User.DoesNotExist:
				form.add_error('email', 'There is no user registered with this email address in our system.')
	else:
		form = PasswordResetRequestForm()

	return render(request, 'studeals/password_reset_request.html', {'form': form, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})

@guest
def password_reset(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None:
		if default_token_generator.check_token(user, token):
			if request.method == 'POST':
				form = PasswordResetForm(data=request.POST,instance=user)

				if form.is_valid():
					user = form.save(commit=False)
					user.set_password(user.password)
					user.save()

					messages.success(request, 'Your password has been reset successfully! You can now login!')
					return HttpResponseRedirect(reverse('login'))
			else:
				form = PasswordResetForm()

			return render(request, 'studeals/password_reset.html', {'form': form, 'uid': uidb64, 'token': token, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})

	raise Http404("Invalid password reset request")

def offers(request):
	offers_list=Offer.objects.order_by('expiration_date')
	category_list=Category.objects.all()
	context_dict={'offers':offers_list, 'categories':category_list}
	return render(request, 'studeals/offers.html', context_dict)

@guest
def user_login(request):
	errors = []

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		recaptcha_response = request.POST.get('g-recaptcha-response')

		if recaptcha_response and recaptcha_check(recaptcha_response):
			user = authenticate(username=username,password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('index'))
				elif user.last_login is None:
					messages.warning(request, 'Your account needs to be activated. You should have received an email at your email address.')
				else:
					errors.append("Your account is disabled.")
			else:
				print("Invalid login details: {0},{1}".format(username, password))
				errors.append("Invalid login details supplied.")
		else:
			errors.append("The CAPTCHA validation failed, please try again.")

	return render(request, 'studeals/login.html', {'errors': errors, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})

@login_required
def user_logout(request):
	logout(request)
	messages.success(request, 'You have been logged out successfully!')
	return HttpResponseRedirect(reverse('login'))
