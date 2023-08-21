from contextlib import closing

from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from django.shortcuts import redirect
from methodism import dictfetchone


def user_type(req):
    if not req.user.is_active:
        logout(req)


    try:
        types = {
            1: "pages/owner/main.html",
            2: "pages/admin/main.html",
            3: "pages/doctor/main.html",
            4: "pages/client/main.html",

        }.get(req.user.user_type, ["pages/client/main.html"])
    except:
        types = ["pages/client/main.html"]
    ctx = {
        "type": types,
        'app_name': settings.APP_NAME
    }
    if not req.user.is_anonymous:
        ctx.update({'user_type': req.user.user_type})
    return ctx


def count(req):
    sql = """
select (select COUNT(*) from core_userdoctor WHERE user_type = 3) as count_doc,
(select COUNT(*) from core_userdoctor WHERE user_type = 2) as count_admin,
(select COUNT(*) from core_userdoctor WHERE user_type = 4) as count_client,
(select COUNT(*) from core_service) as count_service

from django_session limit 1
    
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

    return {
        'count': result
    }
