from django.contrib.auth import login, authenticate


# Create your views here.
from django.shortcuts import render, redirect
from .models import AuthorShow
from .forms import UserForm, UserDetailForm, AuthorForm, AuthorDetailForm, LoginForm


def register(request):
    user_form = UserForm()
    user_detail_form = UserDetailForm()
    author_form = AuthorForm()
    author_detail_form = AuthorDetailForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'user':
            user_form = UserForm(request.POST)
            user_detail_form = UserDetailForm(request.POST)

            if user_form.is_valid() and user_detail_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                user_detail = user_detail_form.save(commit=False)
                user_detail.idUser = user
                user_detail.save()

        elif form_type == 'author':
            author_form = AuthorForm(request.POST)
            author_detail_form = AuthorDetailForm(request.POST)
            if author_form.is_valid() and author_detail_form.is_valid():
                name = author_form.cleaned_data.get('name')
                surname = author_form.cleaned_data.get('surname')
                author_show = AuthorShow.objects.create(name=name, surname=surname)
                author = author_form.save()
                author_detail = author_detail_form.save(commit=False)
                author_detail.idUserAuth = author
                author_detail.idAuthor = author_show
                author_detail.save()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'user_detail_form': user_detail_form,
        'author_form': author_form,
        'author_detail_form': author_detail_form
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
    return render(request, 'home/homePage.html')