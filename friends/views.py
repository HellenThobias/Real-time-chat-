from django.contrib.auth.decorators import login_required
from friends.models import FriendRequest
from django.http import HttpResponse
from django.shortcuts import render
from account.models import Account
import json



@login_required
def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST":
        user_id = int(request.POST.get("receiver_user_id"))
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            # try:
            #Get any friend request (active or not active)
            friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
            #Find if any of them are active
            if not friend_requests.exists():
                create_request(user, payload, receiver)
                return HttpResponse(json.dumps(payload), content_type="application/json")
            else:
                for req in friend_requests:
                    if req.is_active:
                        payload["response"] = "You already sent them a friend request"
                        return HttpResponse(json.dumps(payload), content_type="application/json")
                    #if none are active create a new friend request.
                    req.delete()
                    create_request(user, payload, receiver)
                    return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        payload["response"]= "Method not allowed"
    
    return HttpResponse(json.dumps(payload), content_type = "application/json")


def create_request(user, payload, receiver):
    FriendRequest.objects.create(sender=user, receiver=receiver)
    payload['response']= "Friend request sent."
