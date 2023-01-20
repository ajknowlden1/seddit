from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Thread, Comment, Topic
from .forms import ThreadForm, SignupForm, AddCommentForm

def home(request):
    thread_list = Thread.objects.all()
    if request.method == 'POST' and request.POST['sort'] and not None and request.POST['order'] is not None:
        sort = request.POST['sort']
        order = request.POST['order']
    else:
        sort = 'date'
        order = 'desc'

    match sort:
        case 'date':
            if order == 'asc':
                thread_list = thread_list.order_by('date_pub')
            else:
                thread_list = thread_list.order_by('-date_pub')
                title = "Oldest Thread"
        case 'comments':
            if order == 'asc':
                thread_list = thread_list.annotate(comment_count=Count('comment')).order_by('comment_count')
            else:
                thread_list = thread_list.annotate(comment_count=Count('comment')).order_by('-comment_count')
        case 'votes':
            if order == 'asc':
                thread_list = thread_list.order_by('votes')
            else:
                thread_list = thread_list.order_by('-votes')

    for thread in thread_list:
        thread.comment_count = Comment.objects.filter(for_post_id=thread.id).count()

    return render(request, template_name='main/home.html', context={'thread_list': thread_list, 'sort': sort, 'order': order})

def sign_up(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
        request.method = 'GET'
        return render(request, template_name='registration/signup_success.html')
    else:
        form = SignupForm()
        return render(request, template_name='registration/signup.html', context={'form': form})

def add_comment(request, thread_id):

    thread = Thread.objects.get(pk=thread_id)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['comment_body']
            Comment.objects.create(for_post=thread, comment_author=request.user, content=body)
            request.method == 'GET'
            return HttpResponseRedirect('/{0}'.format(thread_id))
    else:
        form = AddCommentForm()
        return render(request, template_name='main/add_comment.html', context={'form': form, 'thread_id': thread_id})


def thread_vote(request, thread_id):
        inc_vote = int(request.POST.get('inc_vote'))
        Thread.objects.get(pk=thread_id).vote(inc_vote)
        return HttpResponseRedirect('/{0}'.format(thread_id))


def post_thread(request):

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread_title = form.cleaned_data['thread_title']
            thread_author = request.user
            thread_topic = Topic(pk=form.cleaned_data['thread_topic'])
            thread_content = form.cleaned_data['thread_content']
            Thread.objects.create(title=thread_title, author=thread_author, topic=thread_topic, content=thread_content, date_pub=timezone.now())

            return HttpResponseRedirect("/")
    else:
        form = ThreadForm()
        return render(request, template_name='main/post_thread.html', context= {'form': form})


def delete_thread(request, thread_id):

    thread = Thread.objects.get(pk=thread_id)


    if request.method == 'GET':
        return render(request, template_name="main/delete_thread.html", context={'thread': thread})
    elif request.method == 'POST' and 'delete' in request.POST:
        Thread.objects.get(pk=thread_id).delete();
        request.method = 'GET'

        return HttpResponseRedirect("/thread_deleted/")

def thread_deleted(request):
    return render(request, template_name='main/thread_deleted.html')


def thread_view(request, thread_id):
    thread = Thread.objects.get(pk=thread_id)
    top_comments = Comment.objects.filter(for_post_id=thread_id)
    if len(top_comments) > 0:
        has_comments = True
    else:
        has_comments = False
    return render(request, template_name='main/thread.html', context={'thread': thread, 'top_comments': top_comments, 'has_comments': has_comments})

def thread_comment_view(request, thread_id):
    return HttpResponse("Viewing comments for thread %s" % thread_id)


