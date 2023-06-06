import json

from django.contrib.auth import login, authenticate
from django.contrib.sites import requests
import requests

# Create your views here.
from django.shortcuts import render, redirect
# from .models import AuthorShow, Book, AuthorWroteBook
# from .forms import UserForm, UserDetailForm, AuthorForm, AuthorDetailForm, LoginForm



def search(request):
    if request.method=="GET":
        print(request)
        searchInput = request.GET.get("myInput", "john green")
        print(searchInput)
        queries = {'q': searchInput}
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
                'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
                'description': book['volumeInfo']['description'] if 'description' in book['volumeInfo'] else "This book has no description",
                'info': book['volumeInfo']['infoLink'],
                'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0,
                'rating':book['volumeInfo']['averageRating'] if 'averageRating' in book['volumeInfo'] else 3
            }
            books.append(book_dict)


        print(books)

        context={
            'books':books,
            'searchInput':searchInput
        }

        def sort_by_pop(e):
            return e['popularity']

        books.sort(reverse=True, key=sort_by_pop)

        return render(request, 'search/searchResult.html', context)
