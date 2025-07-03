from django.urls import include, path
from . import views
from Monitoring import views as myapp_views
from django.contrib.auth.views import *
from .views import (test_list, start_test, load_profiles, test_results, bulk_edit_users, edit_test_list, admin_users, user_results, export_to_excel_user,
                    delete_test, user_login, admin_users, programs_bulk_update, constructor, export_to_excel, test_list, edit_test_list, edit_test_results,
                    setup_test_results,edit, telegram_login, test_intro, edit_test, delete_user, export_statistics_excel, register, load_directions, statistics_view, edit_user_profile, data_editing)
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', user_login, name='user_login'),

    path('admin-users/', admin_users, name='admin_users'),

    path('test-list/', test_list, name='test_list'),

    path('user_logout/', views.user_logout, name='user_logout'),

    path('register/', register, name='register'),

    path('edit/', edit, name='edit'), 

    path('acc/tests/', test_list, name='test_list'),

    path('acc/test/<int:test_id>/intro/', test_intro, name='test_intro'),

    path('acc/tests/start/<int:test_id>/<int:question_index>', start_test, name='start_test'),

    path('acc/tests/results/<int:user_test_id>/', test_results, name='test_results'),

    path('acc/tests/results/all/', user_results, name='user_results'),

    path('acc/results/<int:test_id>/', user_results, name='user_results'),

    path('admins/admin_users/', admin_users, name='admin_users'),

    path('admins/export_to_excel/', export_to_excel, name='export_to_excel'),

    path('admins/constructor/', constructor, name='constructor'),

    path('admins/constructor/<int:test_id>/', constructor, name='constructor'),

    path('admins/users/<int:user_id>/profile/', views.user_profile, name='user_profile'),

    path('admins/tests/edit/', edit_test_list, name='edit_test_list'),

    path('admins/tests/delete/<int:test_id>/', delete_test, name='delete_test'),

    path('admins/statistics/', statistics_view, name='statistics'),

    path('admins/setup_test_results/<int:test_id>/', setup_test_results, name='setup_test_results'),

    path('admins/tests/edit/<int:test_id>/', edit_test, name='edit_test'),

    path('admins/tests/<int:test_id>/edit/', edit_test, name='edit_test'),

    path('admins/tests/<int:test_id>/results/', edit_test_results, name='edit_test_results'),

    path('admins/tests/', edit_test_list, name='edit_test_list'),

    path('admins/edit_test_list/', edit_test_list, name='edit_test_list'),

    path('admins/test/int:test_id/edit_results/', edit_test_results, name='edit_test_results'),

    path('admins/delete_user/<int:user_id>/', delete_user, name='delete_user'),

    path('admins/export_to_excel_user/', export_to_excel_user, name='export_to_excel_user'), 

    path('admins/user/<int:user_id>/edit/', edit_user_profile, name='edit_user_profile'),

    path('admins/data_editing/', data_editing, name='data_editing'),

    path('programs_bulk_update/', programs_bulk_update, name='programs_bulk_update'),

    path('admins/users/bulk_edit/', bulk_edit_users, name='bulk_edit_users'),

    path('ajax/load-directions/', load_directions, name='ajax_load_directions'),

    path('ajax/load-profiles/', load_profiles, name='ajax_load_profiles'),

    path('admins/export-statistics/', export_statistics_excel, name='export_statistics'),

    path('auth/telegram/', csrf_exempt(telegram_login), name='telegram_login'),
]

