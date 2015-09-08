from django.conf.urls import * 
from django.conf.urls import *
from donorsdetail.resources import *
from tastypie.resources import Resource,ModelResource
from tastypie.api import Api
from donorsdetail.views import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
api = Api(api_name = 'donorapp')
api.register(UserRegisterResource()),
api.register(Donorlogin()),
api.register(Donatedetail()),
api.register(Showdonatedetails())
api.register(Showmycontribution())
api.register(ProjectSchemeCreate())
api.register(Showdonorproject())
api.register(Changepswd())
api.register(Accountsetting())
api.register(Donorsstatus())

urlpatterns = patterns('',
	url(r'^$',userlogin),
    url(r'^donor/$',donor),
    url(r'^userregister/$',userregister),
    url(r'^logout_view/$',logout_view),
    url(r'^accounts/login/$',userlogin),
    url(r'^userlogin/$',userlogin),
    url(r'^adminpage/$',adminpage),
    url(r'^settings/$',settings),
    url(r'^forgetpaswd/$',forgetpaswd),
    url(r'^accountsetting/$',accountsetting),
    # Examples:
    # url(r'^$', 'donor.views.home', name='home'),
    # url(r'^donor/', include('donor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^blog/',include('donor.urls')),
    url(r'^api/',include(api.urls)),
)
