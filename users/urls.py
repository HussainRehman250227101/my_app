from django.urls import path
from . import views
urlpatterns = [
    # PROFILES 
    path('', views.profiles , name = 'profiles'),
    path('single-profile/<str:pk>/', views.single_profile , name = 'single-profile'),
    path('account/', views.useraccount , name = 'account'),
    path('edit-profile/', views.editprofile , name = 'edit_profile'),

    # LOGIN-LOGOUT-REGISTER 
    path('login/', views.loginUser , name = 'login'),
    path('logout/', views.logoutUser , name = 'logout'),
    path('register/', views.registerUser , name = 'register'),
    
    # SKILLS 
    path('add-skill/', views.addskill , name = 'add_skill'),
    path('edit-skill/<str:pk>/', views.editskill , name = 'edit_skill'),
    path('delete-skill/<str:pk>/', views.deleteskill , name = 'delete_skill'),


    # MESSAGES 
    path('inbox/',views.messages_inbox,name='inbox'),
    path('single-message/<str:pk>/',views.single_message,name='single_message'),
    path('single-sent-message/<str:pk>/',views.single_sent_message,name='single_sent_message'),
    path('send-message/<str:pk>/',views.send_message,name='send_message'),
    path('delete-message/<str:pk>/',views.delete_message,name='delete_message'),
]

