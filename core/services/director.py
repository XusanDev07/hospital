from contextlib import closing

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchall, dictfetchone

from core.models import UserDoctor


def cnt(req, tpe=None, new=True):
    kwargs = {'user_type': tpe} if tpe else {}

    # sql = "select id, name, surname, phone from core_userdoctor where new = True and not user_type =1"
    cnt = "SELECT COUNT(*) as cnt from core_userdoctor WHERE new=TRUE  "
    # with closing(connection.cursor()) as cursor:
    #     cursor.execute(sql)
    #     result = dictfetchall(cursor)

    with closing(connection.cursor()) as cursor:
        cursor.execute(cnt)
        cnt_result = dictfetchone(cursor)

    # pagination = UserDoctor.objects.filter(new=new, **kwargs).order_by('-pk')
    # paginator = Paginator(pagination, settings.PAGINATE_BY)
    # page_number = req.GET.get("page", 1)
    # paginated = paginator.get_page(page_number)
    # types = {
    #     3: 'doctor',
    #     2: 'admin',
    #     4: 'member'
    # }
    #
    ctx = {
        # 'roots': paginated,
        # 'root_type': types.get(tpe, 'all'),
        # "result": result,
        "cnt_new": cnt_result
    }
    return render(req, 'base.html', ctx)


def list_members(req, tpe=None, new=True):
    kwargs = {'user_type': tpe} if tpe else {}

    sql = "select id, name, surname, phone from core_userdoctor where new = True and not user_type =1"
    cnt = "SELECT COUNT(*) as cnt from core_userdoctor WHERE new=TRUE  "
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)

    with closing(connection.cursor()) as cursor:
        cursor.execute(cnt)
        cnt_result = dictfetchone(cursor)

    pagination = UserDoctor.objects.filter(new=new, **kwargs).order_by('-pk')
    paginator = Paginator(pagination, settings.PAGINATE_BY)
    page_number = req.GET.get("page", 1)
    paginated = paginator.get_page(page_number)
    types = {
        3: 'doctor',
        2: 'admin',
        4: 'member'
    }

    ctx = {
        'roots': paginated,
        'root_type': types.get(tpe, 'all'),
        "result": result,
        "cnt_new": cnt_result
    }
    return render(req, 'pages/members.html', ctx)



@login_required(login_url="login")
def ban(req, user_id, tpe, status=0):
    try:
        user = UserDoctor.objects.filter(id=user_id).first()
        user.is_active = status
        user.save()
    except:
        pass
    return redirect('members', tpe=tpe)


@login_required(login_url='login')
def grader(request, pk, user_type, dut):
    if request.user.user_type != 1:
        return redirect('home')
    try:
        user = UserDoctor.objects.filter(id=pk).first()
        user.user_type = user_type
        user.save()
    except:
        pass
    return redirect("members", tpe=dut)
