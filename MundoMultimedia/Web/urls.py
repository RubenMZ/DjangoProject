from django.conf.urls import patterns, url
from Web import views
from django.views.generic import TemplateView


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register, name="register"),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile/modify/$',views.modify_user, name='modify_user'),
	url(r'^profile/modify/send/$', views.send_modification, name='send_modification'),
	url(r'^write/$', views.write_new, name='write_new'),
	url(r'^(\d+)-(\d+)-(\d+)/(?P<noticia_id>\d+)/vote/$', views.vote, name='vote'),
	url(r'^(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)/(?P<noticia_id>\d+)/$', views.new, name='new'),
	url(r'^(?P<section_name>\w+)/$', views.filter, name='filter'),

)