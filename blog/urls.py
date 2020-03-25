from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [

    # todo: place these somewhere else!
    path('home/', views.home, name='home'),
    path('stilus/', views.stilus, name='stilus'),

    # blog page
    path('', views.blog, name='blog'),

    # pages of blog entries
    path('page/<int:page>/', views.blog, name='page'),
    path('page/', views.blog),

    # blog entries per tag (and pages thereof)
    path('tag/<int:tag>/', views.tag, name='tag'),
    path('tag/<int:tag>/page/<int:page>/', views.tag, name='tagpage'),

    # one single blog entry
    path('<int:id>/', views.detail, name='detail'),
]
