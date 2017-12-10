from django.conf.urls import url,include
from django.contrib import admin
from .views import *
from django.contrib.auth.views import login,logout
#from django.core.urlresolvers import reverse_lazy
from .views import index1
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^viewproduct/', ProductView.as_view(), name="view_product"),
    url(r'^login/$',login,{'template_name':'profile/login.html'},name='login'),
    url(r'^profile/', profile, name="profile"),
    url(r'^edit-profile/', edit_profile, name="edit_profile"),
    url(r'^addproduct/', AddProductView.as_view(), name="add_product"),
    url(r'^productdetails/(?P<pk>[0-9]+)', ProductDetailView.as_view(), name="product_detail"),
    url(r'^bidderlist/(?P<pk>[0-9]+)', BidderListView.as_view(), name="bidder_list"),
    url(r'^deleteproduct/(?P<pk>[0-9]+)', ProductDelete.as_view(), name="delete_product"),
    url(r'^save_bid/',save_bid, name="save_bid"),
    url(r'^logout/$',logout,{'template_name':'profile/logout.html'},name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^homepage/$', homepage.as_view(), name='homepage'),
    # url(r'^chatroom/$', index, name='chatroom'),
    url(r'^chatroom/(?P<pk>[0-9]+)', index1, name='chatroom'),
    url(r'^about/' , about , name='about') ,
    url(r'^contact/' , contact , name='contact') ,
    url(r'^ajax/validate_notif/$', last_notification, name='last_notification'),
    url(r'^conference/$', conference_room, name='conferencing'),
    #url(r'^activate/(?P<key>.+)$', activation),
    #url(r'^new-activation-link/(?P<user_id>\d+)/$', new_activation_link),
    #url(r'^register/$', views.register, name='register'),


]
