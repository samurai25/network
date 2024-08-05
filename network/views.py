from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django import forms
from .models import User, Post, Follower, Following, Like
import json
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required


class NewPostForm(forms.Form):
    post = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class": "form-control", 
        "required": True,
        "rows": 3,
        "cols": 200
        }))


def index(request):
    user = request.user

    return render(request, "network/index.html", {'form': NewPostForm(), 'user': user})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
    
@login_required   
def new_post(request):
    
    if request.method == "POST":
        
        try:
            newpost = request.POST["newpost"]
        except:
            pass
        
        form = NewPostForm(request.POST)
        
        if form.is_valid():
            post = form.cleaned_data["post"]
           
            date = timezone.now()

            username = request.user.username

            newpost = Post.objects.create(username=username, content=post, created_at=date, likes=0)
            newpost.save()
    
            return HttpResponseRedirect(reverse('network:index'))
        
        else:
            return render(request, "network/index.html", {'form': form})
    
    return render(request, "network/index.html", {'form': NewPostForm()})

@login_required
def following(request):      
    return render(request, "network/following.html")


@login_required
def edit(request):

    if request.method == 'POST':

        try:
            body = json.loads(request.body)
            post_id = body["post_id"]
            content = body["content"]
            
            post = Post.objects.get(id=post_id) 
            
            if content == []:
                content = post.content
            else:
                post.content = content
                post.save()
                
            data = {
                'post_id': post_id,
                'content': content
            }

            return JsonResponse(data, safe=False)
        except:
            return JsonResponse([], safe=False)


def fetch_data(request):                
    data = Post.objects.all().order_by("-created_at").values()
    
    for date in data:
        date['created_at'] = date['created_at'].strftime("%B %d, %Y, %H:%M")
         
    return JsonResponse(list(data), safe=False)
@login_required
def fetch_likes(request):
    
    try:
        user = request.user
        user = User.objects.get(username=user.username)
        likes = Like.objects.filter(user=user).all().values()

        return JsonResponse(list(likes), safe=False)
    except:
        return JsonResponse('not login', safe=False)

@login_required
def post_data(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = request.user
        post_id = body['post_id']

        post = Post.objects.get(id=post_id)
        
        if post.liked.filter(id=user.id).exists():
            post.liked.remove(user)
            post.likes -= 1
            like = Like.objects.filter(user=user, post=post)
            like.delete()
            post.save()
        else:
            post.liked.add(user)
            post.likes += 1
            like = Like.objects.create(user=user, post=post)
            like.save()
            post.save()
            
        
        posts = Post.objects.all()
        liked = []
        
        for post in posts:
            if post.liked.filter(id=user.id).exists():
                liked.append(post.id)
        
        data = {
            "post_id": post_id,
            "liked": liked
        }
            
        return JsonResponse(data, safe=False)


def get_csrf_token(request):
    csrf_token = get_token(request)
    return csrf_token


def profile_data(request, username):
    if request.user.username:
        posts = Post.objects.all().filter(username=username).order_by('-created_at').values()
        
        user = User.objects.get(username=username)
        followers = user.followers.all().count()
        following_count = user.followings.all().count()

        
        for date in posts:
            date['created_at'] = date['created_at'].strftime("%B %d, %Y, %H:%M")
        
        data = {
            'posts': list(posts),
            'followers': followers,
            'following_count': following_count 
        }
        
        return JsonResponse(data, safe=False)
    
    return JsonResponse([], safe=False)
    

def profile(request, username):
    
    if request.user.username:
        profile = User.objects.filter(username=username)
        username = profile[0].username
        current_user = request.user.username

        return render(request, "network/profile.html", {
            'profile': profile, 'username': username, 
            'current_user': current_user})
    
    else:
        return render(request, "network/error.html")
    

def fetch_following_data(request):
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        followings = user.followings.all()
        followers = user.followers.all().count()
        following_count = user.followers.all().count()

        following_list = []
        posts_data = []
        posts = Post.objects.all().values().order_by('-created_at')
        
        for date in posts:
            date['created_at'] = date['created_at'].strftime("%B %d, %Y, %H:%M")
        
        for following in followings:
            u = User.objects.get(id=following.user_id)
            if u.username not in following_list:
                following_list.append(u.username)
        
        
        for post in posts:
            if post['username'] in following_list:
                posts_data.append(post)
                

        data = {
            'following': posts_data,
            'following_list': following_list,
            'following_count': following_count,
            'followers': followers
        }
            
        return JsonResponse(data, safe=False)
    
    else:
        return JsonResponse([], safe=False)
    
def following_data(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body['username']
        user = User.objects.get(username=username)

        current_user = request.user

        if user.followers.filter(user=current_user).exists():
            follower = Follower.objects.get(user=current_user)
            user.followers.remove(follower)
            user.save()
        else:
            try:
                follower = Follower.objects.get(user=current_user)
                user.followers.add(follower)
                user.save()
            except:
                follower = Follower.objects.create(user=current_user)
                follower.save()
                
                user.followers.add(follower)
                user.save()
             

        if current_user.followings.filter(user=user).exists(): 
            following = Following.objects.get(user=user)      
            current_user.followings.remove(following)
            current_user.save()
            
        else:
            try:
                following = Following.objects.get(user=user)
                current_user.followings.add(following)
                current_user.save()
            except:
                following = Following.objects.create(user=user)
                following.save()
                current_user.followings.add(following)
                current_user.save()
            
            
        followings = current_user.followings.all()
        followers = user.followers.all().count()
        following_list = []
        
        for following in followings:
            u = User.objects.get(id=following.user_id)
            if u.username not in following_list:
                following_list.append(u.username)
                
            
        data = {
            'following_list': following_list,
            'followers': followers,
        }
        
        
        return JsonResponse(data, safe=False)
    
    return JsonResponse([], safe=False)
    
    
def error(request):
    return render(request, "network/error.html")