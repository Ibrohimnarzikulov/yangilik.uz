from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import SignupForm, LoginForm, ProfileForm, AvatarForm
from .models import User, Profile


def register_view(request):
    """Ro'yxatdan o'tish sahifasi."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Yangi foydalanuvchiga bo'sh profil yaratamiz
            Profile.objects.create(user=user)
            auth_login(request, user)
            messages.success(request, "Tabriklaymiz! Hisobingiz muvaffaqiyatli yaratildi.")
            return redirect('home')
        else:
            messages.error(request, "Iltimos, xatolarni tuzating.")
    else:
        form = SignupForm()

    return render(request, 'singup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                # keyingi sahifaga qaytish yoki home
                next_url = request.POST.get('next') or request.GET.get('next') or 'home'
                return redirect(next_url)
        messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri.")
    else:
        form = LoginForm(request)

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect('home')


@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            avatar_form = AvatarForm(instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profil ma'lumotlari yangilandi.")
                return redirect('profile')
        elif 'update_avatar' in request.POST:
            profile_form = ProfileForm(instance=request.user)
            avatar_form = AvatarForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, "Avatar yangilandi.")
                return redirect('profile')
        else:
            profile_form = ProfileForm(instance=request.user)
            avatar_form = AvatarForm(instance=profile)
    else:
        profile_form = ProfileForm(instance=request.user)
        avatar_form = AvatarForm(instance=profile)

    context = {
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'profile': profile,
    }
    return render(request, 'profile.html', context)