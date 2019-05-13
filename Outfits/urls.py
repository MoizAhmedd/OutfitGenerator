from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('login/',auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]
