from django.urls import path

from core.services.auto_crud import gets, auto_form, auto_del
from core.services.director import list_members
from core.views import index
from core.services.auth import sign_in, sign_up, sign_out, profile
from core.services.director import ban, grader

urlpatterns = [
    path("", index, name='home'),
    # auth
    path('auth/', sign_in, name='login'),
    path('auth/regis/', sign_up, name='log_up'),
    path('auth/logout/', sign_out, name='log_out'),
    path('auth/profile/', profile, name='profile'),

    # auto
    path('auto/<key>/list', gets, name='dashboard-auto-list'),
    path('auto/<key>/detail/<int:pk>', gets, name='dashboard-auto-detail'),
    path('auto/<key>/add/', auto_form, name='dashboard-auto-add'),
    path('auto/<key>/edit/<int:pk>/', auto_form, name='dashboard-auto-edit'),
    path('auto/<key>/del/<int:pk>/', auto_del, name='dashboard-auto-delete'),

    # members
    path('member/<int:tpe>/', list_members, name='members'),
    # path('member/<int:tpe>/new<int:new>/', list_members_new, name='new_member'),
    path('banner/u-<int:user_id>/s-<int:status>/t-<int:tpe>/', ban, name='banned'),
    path('grader/<int:pk>/<int:user_type>/default<int:dut>/', grader, name='grader')

]
