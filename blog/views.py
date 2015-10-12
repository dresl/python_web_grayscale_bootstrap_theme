from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.views import generic
from django.utils import timezone
from blog.models import Blog
from polls.models import Sidebar
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from blog.forms import BlogForm


def create_blog(request):
    example_form = BlogForm()
    redirect_url = request.GET.get('next')

    # Form handling logic
    if redirect_url is not None:
        example_form.helper.form_action = reverse('blog_create') + '?next=' + redirectUrl

    return render_to_response('/blog/create_blog.html', {'example_form': example_form}, context_instance=RequestContext(request))
    
    # if request.POST:
    #     form = BlogForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()

    #         return HttpResponseRedirect('/blog/')
    # else:
    #     form = BlogForm()

    # args = {}
    # args.update(csrf(request))
    # args['form'] = form
    # if request.user.is_authenticated():
    #     args['sidebar'] = Sidebar.objects.filter(
    #         pub_date__lte=timezone.now()).order_by('-pub_date')
    #     args['username'] = request.user.username
    #     args['full_name'] = request.user.first_name + \
    #         ' ' + request.user.last_name
    #     args['form'] = args['form']
    #     return render(request, 'blog/create_blog.html', args)
    # else:
    #     args['form'] = args['form']
    #     args['sidebar'] = Sidebar.objects.filter(
    #         pub_date__lte=timezone.now()).order_by('-pub_date')
    #     return render(request, 'blog/create_blog.html', args)


def blogs(request):
    args = {}
    args.update(csrf(request))
    args['blogs'] = Blog.objects.all().order_by('-pub_date')
    args['sidebar'] = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + \
            ' ' + request.user.last_name
        return render(request, 'blog/indexb.html', args)
    else:
        return render(request, 'blog/indexb.html', args)

    return render(request, 'blog/indexb.html', args)


def blog(request, blog_id=1):
    args = {}
    args.update(csrf(request))
    args['blogs'] = Blog.objects.all().order_by('-pub_date')
    args['blog'] = Blog.objects.get(id=blog_id)
    args['sidebar'] = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + \
            ' ' + request.user.last_name
        return render(request, 'blog/detailb.html', args)
    else:
        return render(request, 'blog/detailb.html', args)


def like_blog(request, blog_id):
    if blog_id:
        a = Blog.objects.get(id=blog_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()
        return HttpResponseRedirect('/blog/%s' % blog_id)


######### SEARCH AJAX ####################################################

def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    if request.user.is_authenticated():
        blogs = Blog.objects.filter(title__contains=search_text)
        return render(request, 'blog/ajax_search.html', 
                            {'blogs': blogs, 'username': request.user.username,
                             'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        blogs = Blog.objects.filter(title__contains=search_text)
        return render(request, 'blog/ajax_search.html', {'blogs': blogs})
