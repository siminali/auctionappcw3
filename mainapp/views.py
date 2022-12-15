import json
from ast import List
import string

from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import User, Profile
from .forms import LoginForm, SignupForm
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.template import loader
from mainapp.models import User, Item, QandA
from django.core.mail import send_mail

from django.contrib import messages


appname = "Robin's Nest - Mainapp App"

@csrf_exempt
def signup_view(request):
    '''
    Signup function
    Users creating an account
    '''

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # create a new user
            new_user = User.objects.create(username=username)
            # set user's password
            new_user.set_password(password)
            new_user.save()
            # authenticate user
            # establishes a session, will add user object as attribute
            # on request objects, for all subsequent requests until logout
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('mainapp:messages')

    return render(request, 'mainapp/auth/signup.html', {'form': SignupForm})


def login_view(request):
    '''
    Login function
    Users logging into the app
    '''

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('mainapp:messages')

            # failed authentication
            return render(request, 'error.html', {
                'error': 'User not registered. Sign up first.'
            })

        # invalid form
        return render(request, 'mainapp/auth/login.html', {
            'form': form
        })

    return render(request, 'mainapp/auth/login.html', {'form': form})


@login_required
def friends_view(request):
    '''
    Users viewing their list of followers
    '''

    return render(request, 'mainapp/pages/friends.html', {'page': 'friends'})


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('mainapp:login')


@login_required
def members_view(request):
    '''
    Users viewing the list of members
    Can add or remove connections

    WARNING: This uses GET requests for 'add' and 'remove' in order 
    to illustrate CSRF attacks. Adding a connection should use POST
    and removing a connection should use DELETE
    '''

    user = request.user

    # follow new friend
    if 'add' in request.GET:
        friend_username = request.GET['add']
        try:
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            raise Http404('User does not exist')
        user.following.add(friend)
        user.save()

    # unfollow a friend
    if 'remove' in request.GET:
        friend_username = request.GET['remove']
        try:
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            raise Http404('User does not exist')
        user.following.remove(friend)
        user.save()

    return render(request, 'mainapp/pages/members.html', {
        'page': 'members',
        'user': user,
        'members': User.objects.exclude(username=user.username),
    })


@login_required
def profile_view(request):
    user = request.user

    if 'text' in request.POST and request.POST['text']:
        text = request.POST['text'][:4096]
        if user.profile:
            user.profile.text = text
            user.profile.save()
        else:
            profile = Profile(text=text)
            profile.save()
            user.profile = profile
        user.save()

    context = {
        'user': user,
        'page': 'profile',
        'profile': user.profile,
        'session_key': request.session.session_key,
        'meta': request.META,
    }

    return render(request, 'mainapp/pages/profile.html', context)


@login_required
def messages_view(request):
    '''
    Users messages page
    This view uses Vue + Ajax requests
    '''

    user = request.user
    view = request.GET['view'] if 'view' in request.GET else user.username

    if user.username != view:
        view_user = get_object_or_404(User, username=view)
        profile = view_user.profile
        messages = user.messages_with(view_user)
    else:
        profile = user.profile
        messages = user.messages

    vue_data = json.dumps({
        'user': user.to_dict(),
        'view': view,
        'profile': profile.to_dict() if profile else None,
        'messages': [message.to_dict() for message in messages],
    })

    return render(request, 'mainapp/pages/messages.html', {
        'page': 'messages',
        'vue_data': vue_data,
    })


# update email

@csrf_exempt
def update_user_email(request, username):
    if request.method == 'PUT':
        data: any = json.loads(request.body)
        user_profile: User = get_object_or_404(User, name=username)
        user_profile.email: string = data['email']
        user_profile.save()
        return JsonResponse(user_profile.to_dict())

# update DOB

@csrf_exempt
def update_user_DOB(request, username):
    if request.method == 'PUT':
        data: any = json.loads(request.body)
        user_profile: User = get_object_or_404(User, name=username)
        user_profile.dob: any = data['dob']
        user_profile.save()
        return JsonResponse(user_profile.to_dict())

# update profile pic

@csrf_exempt
def update_user_profile_pic(request):
    if request.method == 'PUT':
        data: any = json.loads(request.body)
        user_profile: User = User.objects.get(
            id = data['id']
        )
        user_profile.profile_pic: any = data['profile_pic']
        user_profile.save()
        return JsonResponse(user_profile.to_dict())
