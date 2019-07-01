"""postupload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from postuploadapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('postuploadapp.urls')),
    path('',views.index,name='index'),
 	path('register',views.register,name='register'),
 	path('signup',views.signup,name='signup'),
 	path('index',views.index,name='index'),
 	path('loginvalid',views.loginvalid,name='loginvalid'),
 	path('searchfriend',views.searchfriend,name='searchfriend'),
    path('friendsprofile',views.friendsprofile,name='friendsprofile'),
    path('logout',views.logout,name='logout'),
    path('index',views.index,name='index'),
    path('friendrequest',views.friendrequest,name='friendrequest'),
    path('flist',views.flist,name='flist'),
    path('requeststatustrue',views.requeststatustrue,name='requeststatustrue'),
    path('requeststatusfalse',views.requeststatusfalse,name='requeststatusfalse')


]	+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
