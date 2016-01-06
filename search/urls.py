from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'search.views.search', name='search')
    # url(r'^search/', include('haystack.urls')),
]
