__author__ = 'sirine'
from django.conf.urls import url, patterns
urlpatterns = patterns('blog.views',
url(r'^$','home'),
url(r'^contact/$', 'contact'),
url(r'^registerV/', 'register_votant'),
url(r'^registerC/', 'register_condidate'),
url( r'^profil/(?P<id_condidate>\d+)/$', 'profil'),
url( r'^choice/(?P<Event>\w+)/$', 'choice'),
url(r'^contact/thankyou/$', 'thankyou'),
url( r'^vote/(?P<name_condidate>\w+)/$', 'vote'),
url(r'^login/$', 'user_login'),
url(r'^logout/$','user_logout'),
url(r'^result/(?P<id_event>\d+)/$','result'),
url(r'^about/$','about'),
url(r'^base/$', 'base'),
)
