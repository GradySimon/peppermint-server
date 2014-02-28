from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from peppermint_server import views

urlpatterns = patterns('',
    url(r'^topics/$', views.TopicList.as_view()),
    url(r'userprofiles/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view())
)

# Enable URL format suffixes - specify requested data format with a suffix
urlpatterns = format_suffix_patterns(urlpatterns)