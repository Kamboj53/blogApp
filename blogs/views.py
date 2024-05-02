from django.shortcuts import render, redirect, get_object_or_404
from typing import Any
from django.urls import reverse
from django.http import HttpResponse
from blogs.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout, decorators
from django.views.generic import *
from . models import BlogModel, Comment
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect("blogs:article_list")
    return render(request, 'index.html')

def search_tags(request):
    #Needed to add later
    pass

def search(request):
    #Needed to add later
    pass


class ArticleDetailView(LoginRequiredMixin, DetailView):
    #View for the Detailed view of the blog
    model = BlogModel
    template_name = 'ArticleDetail.html'
    login_url = 'login/'
    
@decorators.login_required(login_url="/login/")        
def comments(request, pk:int):
    #View for adding the comments. TODO- FULL CRUD of comments 
    try:
        blog = get_object_or_404(BlogModel, pk=pk)
        if request.method == 'POST':
            newComment = Comment(post  = blog, body = request.POST.get('body'), user = request.user)
            newComment.save()
            return redirect(reverse("blogs:article_detail",kwargs={"pk":pk}))
    except Exception as e:
        return redirect(reverse("blogs:article_detail",kwargs={"pk":pk}))


class ArticleListView(LoginRequiredMixin, ListView):
    #View for list of the blogs
    model = BlogModel
    template_name = "ArticleList.html"
    context_object_name = 'blogs'
    paginate_by = 5
    login_url = 'login/'
    
def register(request):
    #View for registering account
    if request.user.is_authenticated:
        return redirect("blogs:article_list")
    try:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username =username)
            newUser.set_password(password)

            newUser.save()
            login(request,newUser)

            return redirect("blogs:article_list")
        context = {
                "form" : form
            }
        return render(request,"register.html",context)
    except Exception as e:
        messages.info(request, str(e))
        form = RegisterForm()
        return render(request,"register.html",form)


def loginUser(request):
    #View for login the account
    if request.user.is_authenticated:
        return redirect("blogs:article_list")
    try:
        form = LoginForm(request.POST or None)
        
        context={
            "form":form
        }
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username = username, password = password)
            
            if user is None:
                messages.info(request, "Login Failed! No such user exists")
                return render(request, 'login.html', context)
            
            # messages.success(request, 'Success')
            login(request,user)
            return redirect("blogs:article_list")
        
        return render(request, "login.html",context)
    except Exception as e:
        messages.info(request, str(e))
        form = LoginForm()
        return render(request,"login.html",form)

    
@decorators.login_required(login_url="/login/")
def logoutUser(request):
    #View for logout account
    logout(request)
    # messages.success(request,"Logout Successfully")
    return redirect("blogs:index")
