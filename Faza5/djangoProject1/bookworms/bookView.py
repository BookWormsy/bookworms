import json

from django.contrib.auth import login, authenticate
from django.contrib.sites import requests
import requests
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
from .models import AuthorShow, Book, AuthorWroteBook, Reviews, UsernamesPasswords
# from .forms import UserForm, UserDetailForm, AuthorForm, AuthorDetailForm, LoginForm



def bookView(request, book_title):
    try:
        book = Book.objects.get(title=book_title)
        return render(request, "bookPage/bookPage.html/", {'book':book})
    except Book.DoesNotExist:

        queries = {'q': book_title, 'id': book_title}
        r = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params=queries
        )
        if r.status_code != 200:
            return render(request, "search.html")
        data = r.json();
        print(data)

        response_content = r.content
        data = json.loads(response_content)

        fetched_books = data['items']
        books = []
        for book in fetched_books:
            book_dict = {
                'id': book["id"],
                'title': book['volumeInfo']['title'],
                'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "../../images/closedBook.jpg",
                'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "No Author",
                'description': book['volumeInfo']['description'] if 'description' in book[
                    'volumeInfo'] else "This book has no description",
                'info': book['volumeInfo']['infoLink'],
                'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0,
                'rating': book['volumeInfo']['averageRating'] if 'averageRating' in book['volumeInfo'] else 3
            }
            books.append(book_dict)

            print(books[0])
            book=books[0]
            reviews=listReviews(request)
            users = []
            for review in reviews:
                user = UsernamesPasswords.objects.find(idUser=review.idUser)
                users.append(user)
            context={'book': book, 'rewiews': reviews, 'users': users}
            return render(request, 'bookPage/bookPage.html/', context)

def listReviews(book_title):
    reviews = Reviews.objects.filter(idBook__title=book_title)
    return reviews;


def leaveReview(request):
    return