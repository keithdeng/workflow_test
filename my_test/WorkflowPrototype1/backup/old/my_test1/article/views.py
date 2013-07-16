from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from article.models import Article, Comment
from forms import ArticleForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone


def hello(request):
    name = "Mike"
    html = "<html><body>Hi %s, this seems to have worked!</body></html>" % name
    return HttpResponse(html)


def hello_template(request):
    name = "Mike"
    t = get_template('hello.html')
    html = t.render(Context({'name': name}))
    return HttpResponse(html)


def hello_template_simple(request):
    name = "Mike"
    return render_to_response('hello.html', {'name':name})


class HelloTemplate(TemplateView):

    template_name = 'hello_class.html'

    def get_context_data(self, **kwargs):
        context = super(HelloTemplate, self).get_context_data(**kwargs)
        context['name1'] = 'Mike'
        context['name2'] = 'Li'
        return context


def articles(request):

    return render_to_response('articles.html',
            {'articles' : Article.objects.all()})


def all_functions(request):
    return render_to_response('all_functions.html',
            {'articles' : Article.objects.all()})


def article(request, article_id=1):
    return render_to_response('article.html',
            {'article': Article.objects.get(id=article_id) })


def language(request, language='en-gb'):

    response = HttpResponse('setting language to %s' % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response


def create(request):
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/articles/all')

    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    
    #a = range(10)
    #import matplotlib.pyplot as pt
    #pt.plot(a)
    #pt.show()
    #pt.close()

    return render_to_response('create_article.html', args)


def like_article(request, article_id):
    if article_id:
        a = Article.objects.get(id=article_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()

    return HttpResponseRedirect('/articles/get/%s' % article_id)


def add_comment(request, article_id):
    a = Article.objects.get(id=article_id)

    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.article = a
            c.save()

            return HttpResponseRedirect('/articles/get/%s' % article_id)

    else:
        f = CommentForm()

    args = {}
    args.update(csrf(request))

    args['article'] = a
    args['form'] = f

    return render_to_response('add_comment.html', args)



