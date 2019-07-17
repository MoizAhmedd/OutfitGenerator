from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('login/',auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
    #path('meh',views.CheckUserView,name='checkuser'),
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('dashboard/<int:style>',views.DashboardView,name='dashboard'),
    path('newitem/',views.NewItemView.as_view(),name='newitem'),
    path('myclothes/',views.MyClothesView.as_view(),name='myclothes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
