"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from studeals import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^offers/$', views.offers, name='offers'),
	url(r'^categories/$', views.categories, name='categories'),
	url(r'category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
	url(r'^offer/(?P<offer_title_slug>[\w\-]+)/$', views.show_offer, name='show_offer'),
	url(r'^(?P<category_name_slug>[\w\-]+)/add_offer/$', views.add_offer, name='add_offer'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^my_account/$', views.my_account, name='my_account'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_user, name='activate_user'),
    url(r'^password-reset/$', views.request_password_reset, name='request_password_reset'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset, name='password_reset'),
    url(r'^my-account/$', views.my_account, name='my_account'),
    url(r'^my-account/update-picture/$', views.update_picture, name='update_picture'),
    url(r'^my-account/remove-picture/$', views.remove_picture, name="remove_picture")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
