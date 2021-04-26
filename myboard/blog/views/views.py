#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from blog.models import Post
from django.conf import settings
from blog.forms.form import PostSearchForm
from django.db.models import Q
from django.shortcuts import render

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disqus_short"] = f"{settings.DISQUS_SHORTNAME}"
        context["disqus_id"] = f"post-{self.object.id}-{self.object.slug}"
        context["disqus_url"] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context["disqus_title"] = f"{self.object.slug}"
        return context
    


class PostArchiveView(ArchiveIndexView):
    model = Post
    template_name = 'blog/post_archive.html'


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


class TagCloudTemplateView(TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectListView(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tagname"] = self.kwargs['tag']
        return context

class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        search_word = form.cleaned_data['search_word']
        post_list = Post.objects.filter(
            Q(title__icontains=search_word) | 
            Q(description__icontains=search_word) | 
            Q(content__icontains=search_word)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = search_word
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)