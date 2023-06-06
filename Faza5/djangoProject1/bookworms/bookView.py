import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
import requests
from django import forms
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
from .models import AuthorShow, Book, AuthorWroteBook, Reviews, UsernamesPasswords
# from .forms import UserForm, UserDetailForm, AuthorForm, AuthorDetailForm, LoginForm


import requests
from django.core.files import File



# @login_required
def bookView(request, book_title):
    try:
        book = Book.objects.get(title=book_title)
        reviews = listReviews(request)
        users = []
        # for review in reviews:
        #     user = UsernamesPasswords.objects.find(idUser=review.idUser)
        #     users.append(user)
        context = {'book': book, 'rewiews': reviews, 'users': users}
        return render(request, 'bookPage/bookPage.html/', context)

    except Book.DoesNotExist:

        queries = {'q': book_title, 'title': book_title}
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
                'id': book['volumeInfo']['industryIdentifiers'][0]['identifier'],
                'title': book['volumeInfo']['title'],
                'coverImage': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "../../images/closedBook.jpg",
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
            saveBookInDataBase(book)
            reviews=listReviews(request)
            users = []
            for review in reviews:
                user = UsernamesPasswords.objects.find(idUser=review.idUser)
                users.append(user)
            context={'book': book, 'rewiews': reviews, 'users': users}
            return render(request, 'bookPage/bookPage.html/', context)

def listReviews(book_title):
    reviews=[]
    # reviews = Reviews.objects.filter(idBook__title=book_title)
    return reviews;


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['reviewText']


def getGenre(text):

        keywords = ["romance", "drama", "horror", "thriller"]
        occurrences = {}

        for keyword in keywords:
            count = text.lower().count(keyword)
            if count>0 :
                return keyword
        return "drama"

def download_image(url, my_model):
    response = requests.get(url)
    if response.status_code == 200:
        # Create a new instance of MyModel


        # Open a temporary file in binary write mode
        with open('temp_image.jpg', 'wb') as file:
            file.write(response.content)

        # Assign the image file to the ImageField
        my_model.coverImage.save('image.jpg', File(open('temp_image.jpg', 'rb')))

        # Save the model instance
        my_model.save()

def saveBookInDataBase(newBook):

        book = Book(

            # idBook=newBook['id'],
            title=newBook['title'],
            genre=getGenre(newBook['description']),
            description=newBook['description'],
        )
        download_image(newBook['coverImage'], book)

def create_review(request, book_id):
    pass

    # if request.method == 'POST':
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.idUser = request.user  # Assign the logged-in user
    #         review.idBook_id = book_id  # Assign the book ID from the URL
    #         review.save()
    #         return redirect('success')  # Redirect to a success page
    # else:
    #     form = ReviewForm()
    #
    # return render(request, 'reviews/create_review.html', {'form': form})
