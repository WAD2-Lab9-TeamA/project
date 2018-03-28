from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django import forms
from django.db.models import Avg
from app import settings
from datetime import datetime
from studeals.models import Category, Offer, UserProfile, Vote
from studeals import forms
from studeals.gmaps import geocode
from studeals.auth import activate, authenticate, tokens, send_password_reset_email, recaptcha_check
from studeals.auth.decorators import guest

def index(request):
    offers_list = Offer.objects.order_by('expiration_date')[:5]
    category_list = Category.objects.all()
    context_dict = {
        'offers': offers_list,
        'categories': category_list,
        'gmaps_key': settings.GMAPS_CLIENTSIDE_API_KEY
    }

    return render(request,'studeals/index.html',context=context_dict)

def categories(request):
    category_list=Category.objects.order_by('name')
    offers_list=Offer.objects.order_by('date_added')[:1]
    context_dict={'categories':category_list,'offers': offers_list}
    
    return render(request,'studeals/categories.html',context=context_dict)

def show_category(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        offers = Offer.objects.filter(category=category)
        
        return render(request, 'studeals/category.html', {
            'category': category,
            'offers': offers
        })
    except Category.DoesNotExist:
        return Http404()

def show_offer(request, offer_title_slug):
    try:
        offer = Offer.objects.get(slug=offer_title_slug)
        
        if request.user.is_authenticated:
            try:
                user_rating = Vote.objects.get(user=request.user, offer=offer).vote
            except Vote.DoesNotExist:
                user_rating = None
        else:
            user_rating = None
        
        return render(request, 'studeals/offer.html', {
            'offer': offer,
            'category': offer.category,
            'total_votes': Vote.objects.filter(offer=offer).count(),
            'user_rating': user_rating
        })
    except Offer.DoesNotExist:
        return Http404()

@login_required
def rate_offer(request, offer_title_slug):
    if request.method == 'POST':
        try:
            rating = float(request.POST.get('user_rating'))
        except:
            return HttpResponseBadRequest()

        if rating > 0 and rating <= 5:
            try:
                offer = Offer.objects.get(slug=offer_title_slug)
                try:
                    vote = Vote.objects.get(user=request.user, offer=offer)
                    vote.vote = rating
                    vote.save()
                except Vote.DoesNotExist:
                    vote = Vote.objects.create(
                        user=request.user,
                        offer=offer,
                        vote=rating
                    )

                votes = Vote.objects.filter(offer=offer).aggregate(Avg('vote'))
                offer.rating = round(votes['vote__avg'],1)
                offer.save()

                return JsonResponse({
                    'rating': offer.rating
                })
            except Offer.DoesNotExist:
                return Http404()

    return HttpResponseBadRequest()

@login_required
def add_offer(request):
    form = forms.OfferForm()
    if request.method=='POST':
        form = forms.OfferForm(request.POST)
        if form.is_valid():
            offer=form.save(commit=False)
            offer.category = Category.objects.get(pk=request.POST.get('category'))
            offer.user = request.user
            pos = geocode(offer.place_address)
            if pos['status'] == "OK":
                offer.place_latitude = pos['results'][0]['geometry']['location']['lat']
                offer.place_longitude = pos['results'][0]['geometry']['location']['lng']
            offer.save()
            return offers(request)
        else:
            print(form.errors)
    else:
        form = forms.OfferForm()
    context_dict={'form':form}
    return render(request, 'studeals/add_offer.html', context_dict)

def contact(request):
    if request.method == 'POST':
        form = forms.ContactUsForm(request.POST)

        if form.is_valid():
            # TODO: send email to webmasters
            messages.success(request, 'Thank you for contacting us! We will contact you as soon as possible at the provided email address.')
    else:
        form = forms.ContactUsForm()
    
    return render(request, 'studeals/contact.html', {
        'form': form,
        'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY
        })

def offers(request):
    orderable = {
        'most-recent': 'Most recent',
        'alphabetical': 'Alphabetical',
        'expires-soon': 'Expiring soon',
        'highest-rating': 'Highest rating',
        'lowest-rating': 'Lowest rating'
    }
    orderable_models = {
        'most-recent': '-date_added',
        'alphabetical': 'title',
        'expires-soon': 'expiration_date',
        'highest-rating': '-rating',
        'lowest-rating': 'rating'
    }
    radius_values = ['0.2', '0.5', '1', '2',]

    if 'lat' in request.GET and 'lon' in request.GET:
        address = "%s, %s" % (request.GET.get('lat'), request.GET.get('lon'))
    else:
        address = None
        

    if address or 'address' in request.GET:
        if not address:
            address = request.GET.get('address')

        position = geocode(address)
        if position['status'] == 'OK':
            if 'radius' in request.GET and request.GET.get('radius') in radius_values:
                radius = float(request.GET.get('radius'))
            else:
                radius = 1

            orderable_models['most-recent'] = 'date_added desc'
            orderable_models['highest-rating'] = 'rating desc'
            orderable_models['closest-first'] = 'distance'
            before = {'closest-first': 'Closest'}
            orderable = {**before, **orderable}
        else:
            position = None
            radius = None
    else:
        position = None
        radius = None

    if 'sort' in request.GET and request.GET['sort'] in orderable:
        orderby = orderable_models[request.GET['sort']]
    elif position:
        orderby = orderable_models['closest-first']
    else:
        orderby = list(orderable_models.values())[0]

    if position:
        # query source https://gis.stackexchange.com/questions/31628/find-points-within-a-distance-using-mysql
        offers_list = Offer.objects.raw('''
            select
            *, (
                3959 * acos (
                cos ( radians(%f) )
                * cos( radians( place_latitude ) )
                * cos( radians( place_longitude ) - radians(%f) )
                + sin ( radians(%f) )
                * sin( radians( place_latitude ) )
                )
            ) as distance
            from studeals_offer
            group by id
            having distance < %f
            order by %s
        ''' % (
            position['results'][0]['geometry']['location']['lat'],
            position['results'][0]['geometry']['location']['lng'],
            position['results'][0]['geometry']['location']['lat'],
            radius,
            orderby
        ))
    else:
        offers_list = Offer.objects.order_by(orderby)

    category_list = Category.objects.all()

    context_dict = {
        'offers': offers_list,
        'offers_length': len(list(offers_list)),
        'categories': category_list,
        'query_string': request.GET,
        'orderable': orderable,
        'position': position,
        'gmaps_key': settings.GMAPS_CLIENTSIDE_API_KEY,
        'radius': radius,
        'radius_values': radius_values
    }

    if 'accuracy' in request.GET:
        context_dict['accuracy'] = request.GET.get('accuracy')

    return render(request, 'studeals/offers.html', context_dict)

def my_account(request):
    return render(request, 'studeals/my_account.html', {})

@guest
def register(request):
    if request.method == 'POST':
        form = forms.UserForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.is_active = False
            user.save()

            activate.send_email(request, user)

            messages.success(request, 'Thank you for signing up! To complete your registration you need to confirm your email address. We have just sent you an email containing an activation link!')
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = forms.UserForm()

    return render(request, 'studeals/register.html', {'form': form, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})

@guest
def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        print(user, uid, token)
        if tokens.activation.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully! You can login now!')
            return HttpResponseRedirect(reverse('login'))
        elif not user.is_active and user.last_login is None:
            activate.send_email(request, user)
            messages.warning(request, 'The activation link used has expired. A new one has been sent to your email address.')

    raise Http404("Invalid user activation token")

@guest
def request_password_reset(request):
    if request.method == 'POST':
        form = forms.PasswordResetRequestForm(data=request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                send_password_reset_email(request, user)
                messages.success(request, 'We have just sent you an email containing a password reset link! Check your inbox!')
                return HttpResponseRedirect(reverse('login'))
            except User.DoesNotExist:
                form.add_error('email', 'There is no user registered with this email address in our system.')
    else:
        form = forms.PasswordResetRequestForm()

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
                form = forms.PasswordResetForm(data=request.POST,instance=user)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.save()

                    messages.success(request, 'Your password has been reset successfully! You can now login!')
                    return HttpResponseRedirect(reverse('login'))
            else:
                form = forms.PasswordResetForm()

            return render(request, 'studeals/password_reset.html', {'form': form, 'uid': uidb64, 'token': token, 'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})

    raise Http404("Invalid password reset request")



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

@login_required
def my_account(request):
    if request.method == 'POST':
        form = forms.PasswordUpdateForm(request.POST)
        if form.is_valid():
            password = request.POST.get('your_password')
            new_password = request.POST.get('new_password')

            if request.user.check_password(password):
                request.user.set_password(new_password)
                request.user.save()
                login(request, request.user)

                messages.success(request, 'Your password has been updated successfully!')
            else:
                form.add_error('your_password', 'The entered password is not correct.')
    else:
        form = forms.PasswordUpdateForm()

    return render(request, 'studeals/my_account.html', {'form': form})

@login_required
def update_picture(request):
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST,request.FILES,instance=request.user.userprofile)

        if form.is_valid():
            userprofile = form.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'The file provided is not a valid image.'
            })
    else:
        return JsonResponse({
            'status': 'Bad request'
        }, status=400)

@login_required
def remove_picture(request):
    try:
        if request.user.userprofile.picture:
            request.user.userprofile.picture.delete(save=True)

            return JsonResponse({
                'status': 'ok'
            })
        
        return JsonResponse({
            'status': 'unchanged'
        })
    except:
        return JsonResponse({
            'status': 'error'
        }, status=500)
