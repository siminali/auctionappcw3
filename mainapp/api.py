from django.http.response import HttpResponseBadRequest, JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Message, User, Profile


@login_required
def messages_api(request):
    user = request.user
    view = request.GET['view'] if 'view' in request.GET else user.username

    if request.method == 'POST':
        recip = User.objects.get(username=request.POST['recip'])
        public = request.POST['public'] == "yes"
        text = request.POST['message']
        Message.objects.create(
            sender=user,
            recip=recip,
            text=text,
            public=public,
        )

    if user.username != view:
        view_user = get_object_or_404(User, username=view)
        messages = user.messages_with(view_user)
    else:
        messages = user.messages

    return JsonResponse({
        'messages': [message.to_dict() for message in messages]
    })


@login_required
def message_api(request, message_id):

    message = get_object_or_404(Message, id=message_id)

    if request.method == 'DELETE':
        # Check if user has permission to delete message
        user = request.user
        if message.sender == user or message.recip == user:
            message.delete()
            return JsonResponse({})

        return HttpResponseBadRequest("User does not have permission to delete message")

    return HttpResponseBadRequest("Invalid method")


@login_required
def upload_image(request):
    user = request.user

    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        if not user.profile:
            # if user doesn't have a profile yet
            # need to create a profile first
            profile = Profile(text='')
            profile.save()
            user.profile = profile
            user.save()
        user.profile.image = image_file
        user.profile.save()
        return HttpResponse(user.profile.image.url)
    else:
        raise Http404('Image file not received')
