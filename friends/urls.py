from django.urls import path 

from friends.views import send_friend_request, friend_requests_view, accept_friend_request,remove_friend, decline_friend_request

app_name="friends"

urlpatterns = [
    path('friend_remove/', remove_friend, name="remove-friend"),
    path('friend_request/', send_friend_request, name="friend-request"),
    path('friend_request/<user_id>/', friend_requests_view, name="friend-requests"),
    path('accept_friend_request/<friend_request_id>/', accept_friend_request, name="friend-request-accept"),
    path('decline_friend_request/<friend_request_id>/', decline_friend_request, name="friend-request-decline"),
]
