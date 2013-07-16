from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
        url(r'^all/$', 'fluorescence_fit.views.data_inputs'),
        #url(r'^get/(?P<article_id>\d+)/$', 'article.views.article'),
        )



