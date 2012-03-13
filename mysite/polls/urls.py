from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

# urlpatterns = patterns('',
#     url(r'^$',
#         ListView.as_view(
#             queryset=Poll.objects.order_by('-pub_date')[:5],
#             context_object_name='latest_poll_list',
#             template_name='polls/index.html')),
#     url(r'^(?P<pk>\d+)/$',
#         DetailView.as_view(
#             model=Poll,
#             template_name='polls/detail.html')),
#     url(r'^(?P<pk>\d+)/results/$',
#         DetailView.as_view(
#             model=Poll,
#             template_name='polls/result.html'),
#         name='poll_results'),
#     url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
# )

urlpatterns = patterns('',
    url(r'^$', 'polls.views.index'),
    url(r'^register/$', 'polls.views.register'),                       
    url(r'^(?P<poll_id>\d+)/$', 'polls.views.detail'),
    url(r'^(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='poll_results'),
)
