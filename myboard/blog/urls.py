from django.urls import path, re_path
from blog.views import *

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post_detail'),
    # re_path(r'^post/(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='post_detail'),
    path('archive/', PostArchiveView.as_view(), name='post_archive'),
    path('archive/<int:year>/', PostYearArchiveView.as_view(), name='post_year_archive'),
    # path('archive/<int:year>/<str:month>', PostMonthArchiveView.as_view(), name='post_month_archive'),
    re_path(r'^archive/(?P<year>[-\w]+)/(?P<month>[-\w]+)/$', PostMonthArchiveView.as_view(), name='post_month_archive'),
    path('archive/<int:year>/<str:month>/<int:day>/', PostDayArchiveView.as_view(), name='post_day_archive'),
    path('archive/tody/', PostTodayArchiveView.as_view(), name='post_today_archive'),
    path('tag/', TagCloudTemplateView.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', TaggedObjectListView.as_view(), name='tagged_object_list'),
    path('search/', SearchFormView.as_view(), name='search'),
]
