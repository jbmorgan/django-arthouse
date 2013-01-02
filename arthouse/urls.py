from django.conf.urls.defaults import *

from arthouse import views, forms

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home_url'),
    url(r'^about/$', views.Home.as_view(), name='about_url'),

    url(r'^accounts/login/$', views.login_view, name='login_url'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_url'),
    url(r'^accounts/create/$', views.AccountCreateView.as_view(), name='account_create_url'),
    url(r'^accounts/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'threeltapp/account_update.html',
        'post_change_redirect': '/accounts/change/done/', 'password_change_form': forms.UserUpdateForm}, name='account_update_url'),
    url(r'^accounts/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'threeltapp/account_success.html'},
        name='account_success_url'),

    url(r'^movies/$', views.MovieList.as_view(), name='movie_list_url'),
    url(r'^movies/(?P<movie_pk>\d+)/$', views.MovieDetail.as_view(), name='movie_detail_url'),
    url(r'^movies/create/$', views.MovieCreate.as_view(), name='movie_create_url'),

)

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)