from django.conf.urls import url
from . import views

from django.conf.urls import url, include
from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', LoginView.as_view(template_name='webapp/login.html')),
    url(r'^logout/$', LogoutView.as_view(template_name='webapp/logout.html')),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^feedback/$', views.view_feedback, name='webapp/feedback.html'),
    url(r'^monthly_use_form/$', views.monthly_use, name='webapp/monthly_use_form.html'),
    url(r'^pledge/$', views.energy_pledge, name='webapp/pledge.html'),
    url(r'^social/$', views.social, name='webapp/social.html'),
    url(r'^comparative_feedback/$', views.comparative_feedback, name='webapp/comparative_feedback.html'),
    url(r"^badges/", include("pinax.badges.urls", namespace="pinax_badges")),
    url(r'^group_feedback/$', views.group_feedback, name='webapp/group_feedback.html'),
    url(r'^profile_list/$', views.profile_list, name='webapp/profile_list.html'),


    url(r'^profile/(?P<username>[\w\-]+)/$', views.view_user_profile, name='webapp/profile'),


]
