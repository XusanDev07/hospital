from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import UserDoctor


def sign_in(req):
    if not req.user.is_anonymous:
        return redirect('home')
    ctx = {}
    if req.POST:
        password = req.POST.get('pass')
        phone = req.POST.get('phone')

        user = UserDoctor.objects.filter(phone=phone).first()
        if not user:
            ctx['error'] = 'User yoki parol hato'
            ctx['etype'] = 'phone'
            return render(req, 'pages/auth/login.html', ctx)
        if not user.is_active:
            ctx['error'] = 'usur bloklangan'
            ctx['etype'] = 'ban'
            return render(req, 'pages/auth/login.html', ctx)
        if not user.check_password(password):
            ctx['error'] = 'User yoki parol hato'
            ctx['etype'] = 'password'
            return render(req, 'pages/auth/login.html', ctx)

        login(req, user)
        return redirect('home')

    return render(req, 'pages/auth/login.html', ctx)


def sign_up(req):
    ctx = {}
    if req.POST:
        password = req.POST.get('password')
        pas_con = req.POST.get('pas_con')
        phone = req.POST.get('phone')
        gender = int(req.POST.get('gender'))

        user = UserDoctor.objects.filter(phone=phone).first()

        if user:
            ctx['error'] = 'Bunaqa user bor'
            return render(req, 'pages/auth/register.html', ctx)

        if 'term' not in req.POST:
            ctx['error'] = 'Oferta majburiy'
            return render(req, 'pages/auth/register.html', ctx)
        if password != pas_con:
            ctx['error'] = 'Parollar mos emas'
            return render(req, 'pages/auth/register.html', ctx)

        user = UserDoctor.objects.create_user(phone=phone,
                                              email=req.POST.get('email'),
                                              password=password,
                                              name=req.POST.get('name'),
                                              gender=gender
                                              )

        authenticate(req)
        login(req, user)
        return redirect('home')

    return render(req, "pages/auth/register.html")


@login_required(login_url='login')
def sign_out(req):
    logout(req)
    return redirect('login')


@login_required(login_url='login')
def profile(req):
    ctx = {

    }
    return render(req, "pages/auth/profile.html")
