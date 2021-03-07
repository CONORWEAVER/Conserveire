from django.conf.urls import url
from . import views

from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', LoginView.as_view (template_name='webapp/login.html')),
    url(r'^logout/$', LogoutView.as_view (template_name='webapp/logout.html')),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^feedback/$', views.view_feedback, name='webapp/feedback.html'),
    url(r'^monthly_use_form/$', views.monthly_use, name='webapp/monthly_use_form.html')


]
