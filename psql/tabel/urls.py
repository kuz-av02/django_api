from django.urls import path
from .views import *

# urlpatterns = [
#     path('', UsersOptionsView.as_view()),
#     path('<int:pk>/', UsersOptionsView.as_view()),
# ]

urlpatterns = [
    path('user/options/all/', users_options_view_all),
    path('user/options/<int:pk>/', users_options_view_one),
    path('user/options/create/', users_options_create),

    path('group/all/', group_view_all),
    path('group/user/<int:user_id>/', groups_by_user_id),
    path('group/<int:group_id>/', group_edit),
    path('group/create/', group_create),

    path('group/options/list/', show_all_groups_options),
    path('group/options/<int:group_id>/', show_group_options),
    path('group/options/edit/<int:pk>/', group_options_edit),
    path('group/options/create/', group_options_create),

    path('countries/list/', list_countries_view),
    path('countries/<int:pk>/', list_countries_detail),

    path('geo/all/', show_geo_view_all),
    path('geo/<int:group_id>/', show_geo_by_group),
    path('geo/edit/<int:geo_id>/', geo_edit),
    path('geo/create/', geo_create),

    path('showing-times/all', show_times_view_all),
    path('showing-times/<int:group_id>/', show_times_view_one),
    path('showing-times/edit/<int:pk>/', show_times_edit),
    path('showing-times/create/', show_times_create),

    path('page/all/', show_all_pages_view),
    path('page/<int:page_id>/', show_page_detail),
    path('page/create/', show_times_create),

    path('pages-options/all/', show_all_pages_options),
    path('pages-options/<int:page_id>/', show_page_options_detail),
    path('pages-options/edit/<int:pk>/', page_options_edit),
    path('pages-options/create/', page_options_create),

    path('pages-compiled-stats/all/', show_all_pages_compiled_stats),
    path('pages-compiled-stats/<int:page_id>/', show_page_compiled_stats_detail),

    path('pages-stats/all/', show_all_pages_stats),
    path('pages-stats/<int:page_id>/', show_page_stats_detail),
]