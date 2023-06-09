from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

from .bookView import *
from .searchResultView  import *

urlpatterns = [
    path('', intro, name='intro'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('user/<int:des_user_id>/', user, name='user'),
    path('logout/', customLogoutView.as_view(), name='logout'),
    path('upgrade_request/', upgrade_request, name = 'upgrade_request'),
    path('approve_request/<int:idRequest>/', approve_request, name = 'approve_request'),
    path('delete_request/<int:idRequest>/', delete_request, name = 'delete_request'),
    path('edit_page/', edit_page, name = 'edit_page'),
    path('edit/', edit, name = 'edit'),
    path('searchResult/<str:searchInput>/', search, name='search'),
    path('bookPage/<str:book_title>/', bookView, name='bookView'),
    path('create_review/<int:bookId>/<str:bookTitle>', create_review, name='create_review'),
    path('book/<int:bookId>/', book, name='book'),
    path('challengeList/', challengeList, name='challengeList'),
    path('challengePage/<int:object_id>', challengePage, name='challengePage'),
    path('apply/<int:challengeId>/', apply, name='apply'),
    path('bookRemove/<int:book_id>', bookRemove, name='bookRemove'),
    path('author_show_page/<int:idAuthor>', author_show_page, name='author_show_page'),
    path('author_clicked/<int:idAuthor>', author_clicked, name='author_clicked'),
    path('rate_book/<int:idBook>/', rate_book, name='rate_book'),
    # Other URL patterns
]