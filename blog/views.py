from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.views import generic
from django.utils import timezone
from blog.models import Blog, Comment
from polls.models import Sidebar
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from blog.forms import BlogForm


def create_blog(request):
    if request.POST:
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/blog/')
    else:
        form = BlogForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['sidebar'] = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'blog/create_blog.html', args)

def choose_order_blog_by_age(request):
    if request.method == 'GET':
        args = {}
        list_ = []
        a = timezone.now().year
        b = reversed(range(1990, a+1))
        args['years'] = b
        args['myfield'] = request.GET['myfield']
        for i in b:
            num = Blog.objects.filter(pub_date__year = i).count()
            final = '%s - %s' % (i, num)
            list_.append(final)
        args['blog_counter'] = list_
        if request.GET['myfield'] == 'newest':
            args['blogs'] = Blog.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
            return render(request, 'blog/indexb.html', args)
        elif request.GET['myfield'] == 'oldest':
            args['blogs'] = Blog.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
            return render(request, 'blog/indexb.html', args)

def choose_order_blog_by_year(request):
    if request.method == 'GET':
        args = {}
        list_ = []
        a = timezone.now().year
        b = reversed(range(1990, a+1))
        args['years'] = b
        args['blogs'] = Blog.objects.all().order_by('-pub_date')
        for i in b:
            num = Blog.objects.filter(pub_date__year = i).count()
            final = '%s - %s' % (i, num)
            list_.append(final)
        args['blog_counter'] = list_
        date = int(str(request.GET['myfield'])[0:4])
        args['full_date'] = str(request.GET['myfield'])
        args['blogs'] = Blog.objects.filter(pub_date__year=date)
        return render(request, 'blog/indexb.html', args)

def blogs(request):
    args = {}
    list_ = []
    a = timezone.now().year
    b = reversed(range(1990, a+1))
    args['years'] = b
    args['blogs'] = Blog.objects.all().order_by('-pub_date')
    for i in b:
        num = Blog.objects.filter(pub_date__year = i).count()
        final = '%s - %s' % (i, num)
        list_.append(final)
    args['blog_counter'] = list_
    args['sidebar'] = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'blog/indexb.html', args)

def blog(request, blog_id):
    args = {}
    args.update(csrf(request))
    args['blogs'] = Blog.objects.all().order_by('-pub_date')
    args['blog'] = Blog.objects.get(id=blog_id)
    args['comments'] = args['blog'].comment_set.all().order_by('-pub_date')
    a = Blog.objects.get(id=blog_id)
    args['likes'] = a.users_like_it.all()
    args['sidebar'] = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    likes_list = []
    for i in a.users_like_it.all():
        likes_list.append(i.username)
    args['likes_list'] = likes_list
    return render(request, 'blog/detailb.html', args)


def like_blog(request, blog_id):
    if blog_id:
        a = Blog.objects.get(id=blog_id)
        user = User.objects.get(username=request.user.username)
        a.users_like_it.add(user)
        a.save()
        return HttpResponseRedirect('/blog/%s' % blog_id)

def unlike_blog(request, blog_id):
    if blog_id:
        a = Blog.objects.get(id=blog_id)
        user = user = User.objects.get(username=request.user.username)
        a.users_like_it.remove(user)
        a.save()
        return HttpResponseRedirect('/blog/%s' % blog_id)

def add_comment(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        blog_id = request.POST['blog_id']
        a = Blog.objects.get(id=blog_id)
        a.comment_set.create(owner=user, comment=request.POST['comment'], pub_date=timezone.now())
        return HttpResponseRedirect('/blog/%s' % blog_id)

def delete_comment(request):
    if request.method == "POST":
        blog_id = request.POST['blog_id']
        comment_id = request.POST['comment_id']
        comment_for_delete = Comment.objects.get(id=comment_id)
        comment_for_delete.delete()
        return HttpResponseRedirect('/blog/%s' % blog_id)

######### SEARCH AJAX ####################################################

def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    blogs = Blog.objects.filter(title__icontains=search_text)
    return render(request, 'blog/ajax_search.html', {'blogs': blogs})
