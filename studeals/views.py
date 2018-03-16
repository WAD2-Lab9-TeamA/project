from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from studeals.models import Category, Offer, UserProfile
from studeals.forms import UserForm, UserProfileForm


def index(request):
	
	offers_list=Offer.objects.order_by('expiration_date')[:5]
	category_list=Category.objects.all()
	context_dict={'offers':offers_list, 'categories':category_list}
	return render(request,'studeals/index.html',context=context_dict)
	
def register(request):
	
	registered=False
	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile=profile_form.save(commit=False)
			profile.user=user
			
			if 'picture' in request.FILES:
				profile.picture=request.FILES['picture']
				
			profile.save()
			registered=True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()

	return render(request, 'studeals/register.html', {'user_form':user_form, 'profile_form': profile_form, 'registered':registered})
		
def offers(request):
	offers_list=Offer.objects.order_by('expiration_date')
	category_list=Category.objects.all()
	context_dict={'offers':offers_list, 'categories':category_list}
	return render(request, 'studeals/offers.html', context_dict)
	
def user_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print("Invalid login details: {0},{1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		
		return render(request, 'studeals/login.html', {})

		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))