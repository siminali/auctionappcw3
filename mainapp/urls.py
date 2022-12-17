from django.urls import path

from mainapp import views, api

app_name = 'mainapp'

urlpatterns = [
    # messages page
    path('', views.messages_view, name='messages'),
    # signup page
    path('signup/', views.signup_view, name='signup'),
    # login page
    path('login/', views.login_view, name='login'),
    # logout page
    path('logout/', views.logout_view, name='logout'),
    # members page
    path('members/', views.members_view, name='members'),
    # friends page
    path('friends/', views.friends_view, name='friends'),
    # user profile edit page
    path('profile/', views.profile_view, name='profile'),

    # Views responding to Ajax requests:

    # Ajax: upload new profile image
    path('api/uploadimage/', api.upload_image, name='uploadimage api'),
    # Ajax: post a new message
    path('api/messages/', api.messages_api, name='messages api'),
    # Ajax: delete a message
    path('api/messages/<int:message_id>/', api.message_api, name='message api'),



    #path('api/show', views.show_items),
    

    path('api/User/email/<slug:username>', views.update_user_email, name = "user"),
    path('api/User/dob/<slug:username>', views.update_user_DOB, name = "user"),
    path('api/User/', views.user_api),
    path('api/User/<int:user_id>/', views.user_detail),


]
