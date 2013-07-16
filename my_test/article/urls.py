from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^all_functions/$', 'article.views.all_functions'),
    url(r'^all_beamlines/$', 'article.views.all_beamlines'),
    url(r'^all/$', 'article.views.articles'),

    url(r'^dpc_imagings/$', 'article.views.DPC_imagings'),
    url(r'^dpc_create/$', 'article.views.dpc_create'),
    url(r'^dpc_get/(?P<input_id>\d+)/$', 'article.views.DPC_imaging'),
    url(r'^dpc_run/(?P<input_id>\d+)/$', 'article.views.dpc_see_result'),

    url(r'^get/(?P<article_id>\d+)/$', 'article.views.article'),
    url(r'^run/(?P<article_id>\d+)/$', 'article.views.see_result'),
    url(r'^language/(?P<language>[a-z\-]+)/$', 'article.views.language'),
    url(r'^create/$', 'article.views.create'),
    url(r'^like/(?P<article_id>\d+)/$', 'article.views.like_article'),
    url(r'^add_comment/(?P<article_id>\d+)/$', 'article.views.add_comment'),
    url(r'^see_result/(?P<article_id>\d+)/$', 'article.views.see_result'),
    url(r'^get_result/(?P<article_id>\d+)/$', 'article.views.get_result'),
    url(r'^delete/(?P<article_id>\d+)/$', 'article.views.delete_job'),
    url(r'^edit_job/(?P<article_id>\d+)/$', 'article.views.edit_job'),
    url(r'^submit_job/$', 'article.views.submit_job'),
)
