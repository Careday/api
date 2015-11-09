"""careday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from careapp.views import ChildListView, ChildCreateView, \
    ChildUpdateView, DailyReportCreateView, add_child, \
    DiaperingCreateView, SleepingCreateView, EatingCreateView, \
    ChildPickerView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
        name='careday_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('index')},
        name='careday_logout'),
    url(r'^child$', ChildListView.as_view(), name='childs-list',),
    url(r'^child/new$', ChildCreateView.as_view(), name='child-new',),
    url(r'^dailyintake$', DailyReportCreateView.as_view(),
        name='daily-report',),
    url(r'^child/update/(?P<id>\d+)/$',
        ChildUpdateView.as_view(), name='child-update'),
    url(r'^$', TemplateView.as_view(
        template_name='careapp/index.html'), name='index',),
    # url(r'^$', index, name='index'),
    url(r'^calander$', TemplateView.as_view(
        template_name='careapp/calander.html'), name='calander',),
    url(r'^diapering/new$', DiaperingCreateView.as_view(), name='diapering',),
    url(r'^sleeping/new$', SleepingCreateView.as_view(), name='sleeping',),
    url(r'^eating/new$', EatingCreateView.as_view(), name='eating',),
    url(r'^calander/child$', ChildPickerView.as_view(
        template_name='careapp/childs_picker.html'), name='child-picker',),
    # url(r'^calander/(?P<id>\d+)$', ChildPickerView.as_view(
    #     template_name='careapp/childs_picker.html'), name='child-picker',),
    # url(r'^calander/(?P<id>\d+)$', DailyReportCreateView.as_view(
    #     template_name='careapp/daily_report.html'), name='daily-report',),
]
