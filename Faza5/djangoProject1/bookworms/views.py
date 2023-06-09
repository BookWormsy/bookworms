import uuid
import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import os

from django.db.models import Avg
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render, redirect

from djangoProject1 import settings
from .models import *
from .forms import UserForm, UserDetailForm, RequestForm, LoginForm
from django.contrib.auth.views import LogoutView


def register(request):
    user_form = UserForm()
    user_detail_form = UserDetailForm()
    author_form = UserForm()
    author_detail_form = UserDetailForm()
    request_form = RequestForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'user':
            user_form = UserForm(request.POST)
            user_detail_form = UserDetailForm(request.POST)

            if user_form.is_valid() and user_detail_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                user.groups.add(1)
                user_detail = user_detail_form.save(commit=False)
                user_detail.idUser = user
                user_detail.save()


        elif form_type == 'author':
            author_form = UserForm(request.POST)
            request_form = RequestForm(request.POST)
            author_detail_form = UserDetailForm(request.POST)
            if author_form.is_valid() and request_form.is_valid() and author_detail_form.is_valid():
                author_user = author_form.save(commit=False)
                author_user.set_password(author_form.cleaned_data['password'])
                author_user.save()
                author_user.groups.add(1)
                author_detail = author_detail_form.save(commit=False)
                author_detail.idUser = author_user
                author_detail.save()
                new_request = request_form.save(commit=False)
                new_request.idUser = author_detail
                new_request.type = "author"
                new_request.save()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'user_detail_form': user_detail_form,
        'author_form': author_form,
        'author_detail_form': author_detail_form,
        'request_form': request_form
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})


@login_required
def home(request):
    if request.user.is_superuser:
        authorRequests = Request.objects.all().filter(type="author");
        reviewerRequests = Request.objects.all().filter(type="reviewer");
        return render(request, 'user/adminPage.html',
                      {"authorRequests": authorRequests, "reviewerRequests": reviewerRequests})
    romanceBooks = Book.objects.all().filter(genre="romance");
    classicBooks = Book.objects.all().filter(genre="classic");
    psychologyBooks = Book.objects.all().filter(genre="psychology");
    return render(request, 'home/homePage.html',
                  {'romanceBooks': romanceBooks, 'classicBooks': classicBooks, 'psychologyBooks': psychologyBooks})


def challengeList(request):
    challenges = Challenge.objects.all().filter(endDate__gt=datetime.date.today())
    return render(request, 'challenges/challengeListPage.html', {'challenges': challenges})


def challengePage(request, object_id):
    challenge = Challenge.objects.all().filter(idChallenge=object_id)
    book_ids = ChallengeBooks.objects.all().filter(idChallenge=object_id)
    books = Book.objects.all().filter(idBook__in=book_ids)
    return render(request, 'challenges/challengeProfile.html', {'books': books, 'challenge': challenge})


def intro(request):
    return render(request, 'intro/intro.html')


@login_required
def user(request, des_user_id):
    des_user = UsernamesPasswords.objects.get(idUser=des_user_id)
    if des_user.is_superuser:

        authorRequests = Request.objects.all().filter(type="author");
        reviewerRequests = Request.objects.all().filter(type="reviewer");
        return render(request, 'user/adminPage.html',
                      {"authorRequests": authorRequests, "reviewerRequests": reviewerRequests})
    elif des_user.groups.filter(id=3):
        readlist = ReadList.objects.filter(idUser=des_user)
        book_ids = readlist.values_list('idBook', flat=True)
        readlist_books = Book.objects.filter(idBook__in=book_ids)
        wishlist = WishList.objects.filter(idUser=des_user)
        book_ids = wishlist.values_list('idBook', flat=True)
        wishlist_books = Book.objects.filter(idBook__in=book_ids)
        recommendationList = RecommendationList.objects.filter(idUser=des_user)
        book_ids = recommendationList.values_list('idBook', flat=True)
        recommendationlist_books = Book.objects.filter(idBook__in=book_ids)
        author = Author.objects.get(idUserAuth=des_user)
        bookList = AuthorWroteBook.objects.filter(idAuthor=author.idAuthor)
        book_ids = bookList.values_list('idBook', flat=True)
        written_books = Book.objects.filter(idBook__in=book_ids)
        return render(request, 'user/authorProfilePage.html',
                      {"des_user": des_user, "readlist_books": readlist_books, "wishlist_books": wishlist_books,
                       "recommendationlist_books": recommendationlist_books, "author": author,
                       "written_books": written_books})
    elif des_user.groups.filter(id=2):
        readlist = ReadList.objects.filter(idUser=des_user)
        book_ids = readlist.values_list('idBook', flat=True)
        readlist_books = Book.objects.filter(idBook__in=book_ids)
        wishlist = WishList.objects.filter(idUser=des_user)
        book_ids = wishlist.values_list('idBook', flat=True)
        wishlist_books = Book.objects.filter(idBook__in=book_ids)
        recommendationList = RecommendationList.objects.filter(idUser=des_user)
        book_ids = recommendationList.values_list('idBook', flat=True)
        recommendationlist_books = Book.objects.filter(idBook__in=book_ids)
        reviewer = Reviewer.objects.get(idUserRew=des_user)
        return render(request, 'user/reviewerProfilePage.html',
                      {"des_user": des_user, "readlist_books": readlist_books, "wishlist_books": wishlist_books,
                       "recommendationlist_books": recommendationlist_books, "reviewer": reviewer})
    elif des_user.groups.filter(id=1):
        readlist = ReadList.objects.filter(idUser=des_user)
        book_ids = readlist.values_list('idBook', flat=True)
        readlist_books = Book.objects.filter(idBook__in=book_ids)
        wishlist = WishList.objects.filter(idUser=des_user)
        book_ids = wishlist.values_list('idBook', flat=True)
        wishlist_books = Book.objects.filter(idBook__in=book_ids)
        return render(request, 'user/userProfilePage.html',
                      {"des_user": des_user, "readlist_books": readlist_books, "wishlist_books": wishlist_books})


class customLogoutView(LogoutView):
    next_page = '/login/'


def upgrade_request(request):
    user = request.user
    des_user = User.objects.get(idUser=user)
    des_user_id = request.user.idUser
    redirect_url = f'/user/{des_user_id}'
    request_exists = Request.objects.filter(idUser=des_user).exists()
    if (request_exists):
        return redirect(redirect_url)
    new_request = Request(idUser=des_user, type="reviewer")
    new_request.save()
    return redirect(redirect_url)


def approve_request(request, idRequest):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        des_user_id = request.user.idUser
        redirect_url = f'/user/{des_user_id}'
        app_request = Request.objects.get(idRequest=idRequest)
        if (app_request.type == "reviewer"):
            reviewer = Reviewer(idUserRew=app_request.idUser.idUser, bio="")
            reviewer.save()
            app_request.idUser.idUser.groups.add(2)
            app_request.idUser.delete()
            app_request.delete()
            return JsonResponse({"redirect_url": redirect_url})
        else:
            authorshow_exists = AuthorShow.objects.filter(name=app_request.name, surname=app_request.surname).exists()
            if (authorshow_exists):
                authorshow_objects = AuthorShow.objects.filter(name=app_request.name, surname=app_request.surname)
                authorshow_id = authorshow_objects.first()
            else:
                authorshow_id = AuthorShow(name=app_request.name, surname=app_request.surname, bioShow="")
                authorshow_id.save()
            author = Author(idAuthor=authorshow_id, idUserAuth=app_request.idUser.idUser, bio=authorshow_id.bioShow)
            author.save()
            app_request.idUser.idUser.groups.add(3)
            app_request.idUser.delete()
            app_request.delete()
            return JsonResponse({"redirect_url": redirect_url})
    else:
        return JsonResponse({"error": "Invalid Ajax POST request"})


def delete_request(request, idRequest):
    des_user_id = request.user.idUser
    redirect_url = f'/user/{des_user_id}'

    if request.method == 'POST':
        try:
            app_request = Request.objects.get(idRequest=idRequest)
            app_request.delete()
            return JsonResponse({'message': 'Request deleted successfully.'})
        except Request.DoesNotExist:
            return JsonResponse({'error': 'Request not found.'}, status=400)
    else:
        return redirect(redirect_url)


def edit_page(request):
    user = request.user
    des_user_id = request.user.idUser

    username = UsernamesPasswords.objects.get(idUser=des_user_id)  # dohvatamo username sa nasim id
    bio = Reviewer.objects.get(idUserRew=des_user_id)  # dohvatamo odgovarajucu biografiju
    recommendationList = RecommendationList.objects.filter(idUser=des_user_id)
    book_ids = recommendationList.values_list('idBook', flat=True)  # uzimamo ids svih knjiga u listi
    recommendationList_books = Book.objects.filter(idBook__in=book_ids)  # dohvatamo objekte knjiga

    if (user.groups.filter(id=2)):
        return render(request, 'edit/editReviewer.html', {
            'username': username,
            'bio': bio,
            'recommendationList_books': recommendationList_books
        })


def edit(request):
    des_user_id = request.user.idUser
    redirect_url = f'/user/{des_user_id}'
    image_file = request.FILES.get('image')
    if request.method == 'POST':
        new_username = request.POST.get('newUsername')  # iz requesta uzimamo info o novom username-u/ bio
        new_bio = request.POST.get('newBio')

        user = UsernamesPasswords.objects.get(idUser=des_user_id)  # dohvatamo username sa nasim id
        bio = Reviewer.objects.get(idUserRew=des_user_id)  # dohvatamo odgovarajucu biografiju

        if (user != None):  # u slucaju da je nesto uneseno u polje za promenu korisnickog imena, postavljamo novo ime
            user.username = new_username
            user.save()
        if (bio != None):  # u slucaju da je nesto uneseno u polje za promenu biografije, postavljamo novi bip
            bio.bio = new_bio
            bio.save()
    if image_file:
        # Generate a unique filename for the uploaded image
        filename = f'uploaded_image_{uuid.uuid4().hex}.jpg'

        # Save the uploaded image to the media directory
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(image_path, 'wb') as file:
            for chunk in image_file.chunks():
                file.write(chunk)
        request.user.profileImage = "/images/" + filename
        request.user.save()

    return redirect(redirect_url)


def editUser(request):
    des_user_id = request.user.idUser
    redirect_url = f'/user/{des_user_id}'
    image_file = request.FILES.get('image')
    data = {
        'username': '',
    }
    if request.method == 'POST':
        new_username = request.POST.get('newUsername')  # iz requesta uzimamo info o novom username-u/ bio

        user = UsernamesPasswords.objects.get(idUser=des_user_id)  # dohvatamo username sa nasim id

        if (user != None):  # u slucaju da je nesto uneseno u polje za promenu korisnickog imena, postavljamo novo ime
            user.username = new_username
            data['username'] = new_username
            user.save()
    if image_file:
        # Generate a unique filename for the uploaded image
        filename = f'uploaded_image_{uuid.uuid4().hex}.jpg'

        # Save the uploaded image to the media directory
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(image_path, 'wb') as file:
            for chunk in image_file.chunks():
                file.write(chunk)
        request.user.profileImage = "/images/" + filename
        request.user.save()

    return redirect(redirect_url, {'my_dict': data})


def bookRemove(request, book_id):
    redirect_url = f'/edit_page/'
    reccomentation = RecommendationList.objects.get(idBook=book_id, idUser=request.user.idUser)
    reccomentation.delete()
    return redirect(redirect_url)


def author_show_page(request, idAuthor):
    author = AuthorShow.objects.get(idAuthor=idAuthor)
    written_books = Book.objects.filter(authorwrotebook__idAuthor=author)
    return render(request, "authorshow/authorShowPage.html", {"author": author, "written_books": written_books})


def author_clicked(request, idAuthor):
    author = Author.objects.filter(idAuthor=idAuthor)
    des_user_id = request.user.idUser
    if (author):  # ako postoji autor ide se na njegovu stranicu
        s_author = Author.objects.get(idAuthor=idAuthor)
        redirect_url = f'/user/{s_author.idUserAuth_id}'
        return redirect(redirect_url)
    else:  # ako ne postoji ide se na stranicu prikaznog autora
        redirect_url = f'/author_show_page/{idAuthor}'
        return redirect(redirect_url)


def apply(request, challengeId):
    print("pls")
    user_id = request.user
    challenge = Challenge.objects.get(idChallenge=challengeId)
    redirect_url = f'/home/'
    if request.method == "POST":
        model = TakesChallenge(
            idUser=user_id,
            idChallenge=challenge
        )
        model.save()

    readlist = ReadList.objects.all().filter(idUser=user_id)
    rbook_ids = readlist.values_list('idBook', flat=True)
    active_chl = Challenge.objects.all().filter(status="true");
    for clg in active_chl:
        # if clg.endDate == datetime.date.today():
        flag = 1
        book_ids = ChallengeBooks.objects.all().filter(idChallenge=clg.idChallenge)
        for book_id in book_ids:
            if not rbook_ids.contains(book_id):
                flag = 0
        if flag == 1:
            idBadge = clg.idBadge
            model2 = HasBadge(
                idUser=user_id,
                idBadge=idBadge
            )
            model2.save()
            # post u bazu

    return redirect(redirect_url)


def rate_book(request, idBook):
    try:
        book = Book.objects.get(idBook=idBook)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    rating_value = request.POST.get('rating')
    new_rating = Rating(rating = rating_value, idBook=book)
    new_rating.save()
    ratings = Rating.objects.filter(idBook=book)
    rating_sum = sum([rating.rating for rating in ratings])
    rating_count = ratings.count()

    if rating_count > 0:
        average_rating = rating_sum / rating_count
    else:
        average_rating = 0

    return JsonResponse({'rating': average_rating})
