from django.urls import path
from . import views
urlpatterns = [
    path('',views.projects, name = 'projects'),
    path('project/<str:pk>/',views.single_project, name = 'project'),
    path('addproject/',views.addproject, name = 'addproject'),
    path('deleteproject/<str:pk>',views.deleteproject, name = 'deleteproject'),
    path('editproject/<str:pk>/',views.editproject, name = 'editproject'),
    path('edit_review/<str:pk>/',views.edit_review, name = 'edit_review'),
    path('delete_review/<str:pk>/',views.delete_review, name = 'delete_review'),

]