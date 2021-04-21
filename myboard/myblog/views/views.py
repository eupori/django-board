#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from myblog.models import Post

# Create your views here.

def index(request):
    return HttpResponse("cmlee's first blog in django")

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostArchiveView(ArchiveIndexView):
    model = Post
    template_name = 'blog/post_archive.html'
    date_field = 'modify_dt'


class PostYearArchiveView(YearArchiveView):
    model = Post
    template_name = 'blog/post_archive_year.html'
    date_field = 'modify_dt'
    make_object_list = True


class PostMonthArchiveView(MonthArchiveView):
    model = Post
    template_name = 'blog/post_archive_month.html'
    date_field = 'modify_dt'


class PostDayArchiveView(DayArchiveView):
    model = Post
    template_name = 'blog/post_archive_day.html'
    date_field = 'modify_dt'


class PostTodayArchiveView(TodayArchiveView):
    model = Post
    template_name = 'blog/post_archive_today.html'
    date_field = 'modify_dt'







