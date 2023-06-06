from django.urls import path
from .views import register, login_view, home, intro
from django.contrib.auth import views as auth_views
from .bookView import *
from .searchResultView  import *

urlpatterns = [
    path('', intro, name='intro'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('searchResult/', search, name='search'),

    path('bookPage/<str:book_title>/', bookView, name='bookView'),
    # Other URL patterns
]