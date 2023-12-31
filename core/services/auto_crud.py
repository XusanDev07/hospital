from contextlib import closing

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchone

from core.models import *
from core.forms import *
from core.services.director import cnt


@login_required(login_url='login')
def gets(requests, key, pk=None):
    try:
        cnt = "SELECT COUNT(*) as cnt from core_userdoctor WHERE new=TRUE"
        with closing(connection.cursor()) as cursor:
            cursor.execute(cnt)
            cnt_result = dictfetchone(cursor)

        Model = {
            "service": Service,
            "pr": Price,
            "cnt_new": cnt_result

        }[key]
    except:
        return render(requests, 'base.html', {"error": 404})
    if pk:
        root = Model.objects.filter(pk=pk).first()
        ctx = {
            # "ctn_new": cnt()
            "pos": "one",
            'root': root,
        }
        if not root:
            ctx['error'] = 404
    else:
        pagination = Model.objects.all().order_by('-pk')
        paginator = Paginator(pagination, settings.PAGINATE_BY)
        page_number = requests.GET.get("page", 1)
        paginated = paginator.get_page(page_number)

        ctx = {
            "roots": paginated,
            "pos": "list"
        }

    return render(requests, f'pages/{key}.html', ctx)


@login_required(login_url='login')
def auto_form(requests, key, pk=None):
    try:
        Model = {
            "service": "Service",
            "pr": "Price",
        }[key]


    except:
        return render(requests, 'base.html', {"error": 404})
    root = None
    if pk:
        root = eval(Model).objects.filter(pk=pk).first()
        if not root:
            ctx = {"error": 404}
            return render(requests, f'pages/{key}.html', ctx)

    form = eval(f"{Model}Form")(requests.POST or None, requests.FILES or None, instance=root)
    if form.is_valid():
        form.save()
        return redirect('dashboard-auto-list', key=key)

    ctx = {
        "form": form,
        "pos": 'form'
    }

    print(ctx)
    return render(requests, f'pages/{key}.html', ctx)


@login_required(login_url='login')
def auto_del(requests, key, pk):
    try:
        Model = {
            "service": Service,
            "pr": Price
        }[key]
    except:
        return render(requests, 'base.html', {"error": 404})

    root = Model.objects.filter(pk=pk).first()
    if not root:
        ctx = {"error": 404}
        return render(requests, f'pages/{key}.html', ctx)
    root.delete()
    return redirect('dashboard-auto-list', key=key)
