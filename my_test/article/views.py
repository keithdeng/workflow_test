from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from article.models import Article, Comment, DPC_data
from forms import ArticleForm, CommentForm, DPC_Form
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
#from article.FBP import recon



def articles(request):

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
    args['articles'] = Article.objects.all()

    return render_to_response('articles.html',args)


def all_functions(request):
    return render_to_response('all_functions.html',
            {'articles' : Article.objects.all()})

def all_beamlines(request):
    return render_to_response('all_beamlines.html')


def article(request, article_id=1):
    args = {}
    item = Article.objects.get(id=article_id)
    args['article'] = item
    args['articles'] = Article.objects.all()
    return render_to_response('article.html',args)


def submit_job(request):
    args = {}
    #args['article'] = Article.objects.get(id=article_id)
    args['articles'] = Article.objects.all()
    total_len = len(Article.objects.all())
    args['article'] = Article.objects.get(id=total_len)

    return render_to_response('submit_job.html',args)


def edit_job(request, article_id=1):

    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/articles/all')

    else:
        form = ArticleForm()
        args = {}
        args.update(csrf(request))

    item = Article.objects.get(id=article_id)
    args['article'] = item
    args['articles'] = Article.objects.all()

    args['form'] = form

    return render_to_response('edit_job.html',args)


def see_result(request, article_id=1):

    cur_obj = Article.objects.get(id=article_id)

    angle_start = int(cur_obj.angle_start)
    angle_end = int(cur_obj.angle_end)
    angle_step = int(cur_obj.angle_step)
    print cur_obj.algorithm, str(cur_obj.save_to), type(cur_obj.angle_start)
    print int(angle_start)


    job = str(cur_obj.algorithm)
    user = "user1"
    passcode = "pw"

    output_file = str(user)+"_"+str(article_id)+".jpeg"
    #output_file = str(cur_obj.save_to)

    information = str(int(angle_start))+" "+str(int(angle_end))+" "+str(int(angle_step))

    #print cur_obj, information

    import numpy as np
    #import Image
    #from WorkflowPrototype1.FBP import recon

    """
    #oname = '../WorkflowPrototype1/projs/projections_'+str(angle_start)+'_'+str(angle_end)+'_'+str(angle_step)+'.npy'

    oname = '../my_test/static/uploaded_files/projections_'+str(angle_start)+'_'+str(angle_end)+'_'+str(angle_step)+'.npy'
    print oname
    projs = np.load(oname)


    #reconstruction = recon(projs, angle_start, angle_end, angle_step)
    #print "job done!"
    im = Image.fromarray(np.uint8(reconstruction))
    file_path = "/Users/Li/Research/X-ray/Research_work/XRF/my_workflow/my_test/static/images/"+output_file  #"../static/images/out.jpeg"#+str(cur_obj.save_to)
    im.save(file_path)

    """

    #save_folder = "../static/images"

    from WorkflowPrototype1.workflow.workflow_user import Workflow_user
    from WorkflowPrototype1.workflow.workflow_setting import brokers
    import json


    file_p = "../static/images/"

    message = {"instrument": "HXN",
        "job": job,
        "user": user,
        "passcode": passcode,
        "input_data_file": "filename.png",
        "output_data_file": file_p+output_file,
        "information": information, #"0 180 1",#a.notes,
        "method": ""
    }

    wu = Workflow_user(brokers, user, passcode)
    msg = json.dumps(message)
    wu.submit(msg)

    print "Job done!"

    return render_to_response('see_result.html',
            {'article': Article.objects.get(id=article_id) })


def get_result(request,article_id=1):

    cur_obj = Article.objects.get(id=article_id)
    return render_to_response('get_result.html',
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

            return HttpResponseRedirect('/articles/submit_job/')

    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_article.html', args)


def delete_job(request, article_id=1):
    obj = Article.objects.get(id=article_id)
    obj.delete()
    return HttpResponseRedirect('/articles/all')


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


###--------Differential Phase Contrast Imaging part -------------###

def DPC_imagings(request):
    return render_to_response('DPC_imagings.html',
            {'input': DPC_data.objects.all() })


def DPC_imaging(request, input_id=1):
    return render_to_response('DPC_imaging.html',
            {'input': DPC_data.objects.get(id=input_id) })



def dpc_create(request):
    if request.POST:
        form = DPC_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/articles/dpc_imagings')

    else:
        form = DPC_Form()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    output = render_to_response('dpc_create.html', args)

    return output #render_to_response('create_article.html', args)



def dpc_see_result(request, input_id=1):

    cur_obj = DPC_data.objects.get(id=input_id)

    #angle_start = cur_obj.angle_start
    #angle_end = cur_obj.angle_end
    #angle_step = cur_obj.angle_step
    #print cur_obj.algorithm, str(cur_obj.save_to), type(cur_obj.angle_start)


    #job = str(cur_obj.algorithm)
    #user = "user1"
    #passcode = "pw"
    #information = str(angle_start)+" "+str(angle_end)+" "+str(angle_step)

    #print cur_obj, information

    """
    from WorkflowPrototype1.workflow_user import Workflow_user
    from WorkflowPrototype1.workflow_setting import _brokers
    import json

    message = {"instrument": "HXN",
        "job": job,
        "user": user,
        "passcode": passcode,
        "input_data_file": "filename.png",
        "output_data_file": "a.png",
        "information": "0 180 1",#a.notes,
        "method": ""
    }

    wu = Workflow_user(_brokers, user, passcode)
    msg = json.dumps(message)
    wu.submit(msg)
    """

    return render_to_response('dpc_see_result.html',
            {'input': DPC_data.objects.get(id=input_id) })


