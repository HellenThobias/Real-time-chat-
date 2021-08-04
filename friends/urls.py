from django.urls import path 

from friends.views import send_friend_request

app_name="friends"

urlpatterns = [
    path('friend_request/', send_friend_request, name="friend-request")
]
