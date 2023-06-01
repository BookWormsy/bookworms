from django.contrib.auth import login, authenticate


# Create your views here.
from django.shortcuts import render, redirect
from .models import Book, ReadList, WishList
from .forms import UserForm, UserDetailForm, RequestForm,  LoginForm


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
            request_form = UserDetailForm(request.POST)

            if user_form.is_valid() and user_detail_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                user_detail = user_detail_form.save(commit=False)
                user_detail.idUser = user
                user_detail.save()
                user_detail.groups.add(1)

        elif form_type == 'author':
            author_form = UserForm(request.POST)
            request_form = RequestForm(request.POST)
            author_detail_form = UserDetailForm(request.POST)
            if author_form.is_valid() and request_form.is_valid() and author_detail_form.is_valid():
                author_user = author_form.save(commit=False)
                author_user.set_password(author_form.cleaned_data['password'])
                author_user.save()
                author_detail = author_detail_form.save(commit=False)
                author_detail.idUser = author_user
                author_detail.save()
                author_detail.groups.add(1)
                new_request = request_form.save(commit=False)
                new_request.idUser = author_detail
                new_request.save()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'user_detail_form': user_detail_form,
        'author_form': author_form,
        'author_detail_form' : author_detail_form,
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

def home(request):
    romanceBooks = Book.objects.all().filter(genre="romance");
    return render(request, 'home/homePage.html', {'romanceBooks' : romanceBooks})

def intro(request):
    return render(request, 'intro/intro.html')