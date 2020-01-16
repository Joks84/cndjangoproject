from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Comment, SignUp
from .forms import SignUpForm, CommentForm
from django.views import generic
from django.conf import settings
import requests
import json
from .forms import EmailSignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


#homepage with signup form for newsletter
def index(request):
    template_name = 'cn_app/index.html'
    form = EmailSignUpForm()
    return render(request, template_name, {'form':form})

class AboutView(generic.TemplateView):
    template_name = 'cn_app/about.html'

#Displays posts from the category 'City'
def city_list(request):
    posts = Post.objects.filter(category__name='Cities').order_by('-published_date')
    template_name = 'cn_app/cities.html'
    return render(request, 'cn_app/cities.html', {'posts':posts})

#Displays posts from the category 'Province'
def province_list(request):
    posts = Post.objects.filter(category__name='Provinces').order_by('-published_date')
    template_name = 'cn_app/provinces.html'
    return render(request, 'cn_app/provinces.html', {'posts':posts})

#Displays posts from the category 'Historic Spots'
def history_list(request):
    posts = Post.objects.filter(category__name='Historic Spots').order_by('-published_date')
    template_name = 'cn_app/history.html'
    return render(request, 'cn_app/history.html', {'posts':posts})

#Displays posts from the category 'Nature'
def nature_list(request):
    posts = Post.objects.filter(category__name='Nature').order_by('-published_date')
    template_name = 'cn_app/nature.html'
    return render(request, 'cn_app/nature.html', {'posts':posts})

#Displays posts from the category 'Expats in China'
def expats_list(request):
    posts = Post.objects.filter(category__name='Expats in China').order_by('-published_date')
    template_name = 'cn_app/expats.html'
    return render(request, 'cn_app/expats.html', {'posts':posts})

#list of posts
def post_list(request):
    posts = Post.objects.filter().order_by('-published_date')
    template_name = 'cn_app/post_list.html'
    return render(request, 'cn_app/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    template_name = 'cn_app/post_detail.html'
    return render(request, 'cn_app/post_detail.html', {'post':post})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('cn_app:index'))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('cn_app:index')

    else:
        form = SignUpForm()
    return render(request, 'cn_app/signup.html', {'form':form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
        else:
            messages.error(request, "invalid username or password.")
    form = AuthenticationForm()
    return render(request = request, template_name='cn_app/login.html', context = {'form':form})


@login_required
def add_comment(request, pk):
    template_name = 'cn_app/comment.html'
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter()
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('cn_app:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, template_name, {'post':post,
                                                    'comments':comments,
                                                    'new_comment':new_comment,
                                                    'form':form})


# Newsletter Signup
MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'

def subscribe(email):
    data = {
        'email_address':email,
        'status':'subscribed'
    }
    r = requests.post(
        members_endpoint,
        auth = ("", MAILCHIMP_API_KEY),
        data = json.dumps(data)
    )
    return r.status_code, r.json()


def email_list_signup(request):
    form = EmailSignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email_signup_qs = SignUp.objects.filter(email = form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, 'You are alrady subscribed')
            else:
                subscribe(form.instance.email)
                form.save()
                messages.info(request, 'Well done! You are now subscribed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
