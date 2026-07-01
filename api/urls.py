from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from . import views

urlpatterns = [
    path('checkout_api',views.check_api, name='check_api'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',views.all_routes,name='api'),
    path('projects/',views.all_projects),
    path('projects/<str:pk>/',views.single_project),
    path('projects/<str:pk>/vote/',views.post_vote),
    
]
