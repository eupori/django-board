#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from water.models import User, Profile, Water
from rest_framework import serializers
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import json

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Water
        fields="__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields="__all__"


def get_chart_data(user, water):
    # today_amount = sum([item.amount for item in water])
    day_7 = datetime.datetime.now()-datetime.timedelta(days=7)
    water_today = Water.objects.filter(user=user, time__gte=datetime.datetime.today().date()).order_by('-time')
    water_week = Water.objects.filter(user=user, time__gte=day_7.date()).order_by('-time')

    

    today_json = {}
    week_json = {}

    for each in water_week:
        if each.time.date() in week_json.keys():
            week_json[each.time.date()] += each.amount
        else:
            week_json[each.time.date()] = each.amount
    week_list = [[str(key), week_json[key]] for key in sorted(week_json.keys())]

    for each in water_today:
        if each.time.hour in today_json.keys():
            today_json[each.time.hour] += each.amount
        else:
            today_json[each.time.hour] = each.amount
    today_list = [[str(key), today_json[key]] for key in sorted(today_json.keys())]

    week_values = list(water_week.values_list("amount", flat=True))
    week_avg = sum(week_values) / len(week_list)

    print("@@@@@@@@@@@@@@@@@@@")
    print(week_values)
    print(sum(week_values))
    print(len(week_values))
    print(len(week_list))
    print("@@@@@@@@@@@@@@@@@@@")
    

    return {"today_list":today_list, "week_list":week_list, "week_avg":week_avg}


class WaterView(LoginRequiredMixin, TemplateView):
    template_name = 'templates.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    # request
    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)

        user = self.request.user.profile

        day_7 = datetime.datetime.now()-datetime.timedelta(days=7)
        water_today = Water.objects.filter(user=user, time__gte=datetime.datetime.today().date()).order_by('-time')
        water_week = Water.objects.filter(user=user, time__gte=day_7.date()).order_by('-time')

        water = Water.objects.filter(user=user, time__gte=datetime.datetime.today().date()).order_by('-time')
        today_amount = sum(list(water.values_list("amount", flat=True)))

        water_json = WaterSerializer(water, many=True).data
        user_json = UserSerializer(user).data

        chart_data = get_chart_data(user, water)

        context = {}
        context['water'] = water_today
        context['object'] = Profile.objects.last()
        context['today'] = datetime.datetime.today()
        context['today_amount'] = today_amount
        context['today_list'] = json.dumps(chart_data['today_list'])
        context['week_list'] = json.dumps(chart_data['week_list'])
        context['week_avg'] = int(chart_data['week_avg'])
        return context


    def post(self, request, *args, **kwargs):
        user = Profile.objects.get(user__id=request.POST.get('user'))
        amount = int(request.POST.get('amount'))
        Water.objects.create(user=user, amount=amount)

        user.total += amount
        user.save()

        water = Water.objects.filter(user=user, time__gte=datetime.datetime.today().date()).order_by('-time')
        today_amount = sum(list(water.values_list("amount", flat=True)))

        water_json = WaterSerializer(water, many=True).data
        user_json = UserSerializer(user).data

        chart_data = get_chart_data(user, water)

        result = {'success':"success", 'water':water_json, 'object':user_json,
                'today':str(datetime.datetime.today()), 'today_amount':today_amount, 'today_list':chart_data['today_list']}
        render_page = render_to_string("history.html", {'water':water})
        render_page_chart_today = render_to_string("today_chart.html", {'today_list':json.dumps(chart_data['today_list'])})
        render_page_chart_week = render_to_string("week_chart.html", {'week_list':json.dumps(chart_data['week_list']), 'week_avg':int(chart_data['week_avg'])})
        return JsonResponse({'result':result, 'render_history':render_page, 'render_chart_today':render_page_chart_today, 'render_chart_week':render_page_chart_week})

class WaterDeleteView(TemplateView):
    def post(self, request, *args, **kwargs):
        target_id = request.POST.get('id')
        target_object = Water.objects.get(id=target_id)

        target_object.delete()

        user = target_object.user
        water = Water.objects.filter(user=user, time__gte=datetime.datetime.today().date()).order_by('-time')
        today_amount = sum(list(water.values_list("amount", flat=True)))

        water_json = WaterSerializer(water, many=True).data
        user_json = UserSerializer(user).data

        chart_data = get_chart_data(user, water)

        result = {'success':"success", 'water':water_json, 'object':user_json,
                'today':str(datetime.datetime.today()), 'today_amount':today_amount, 'today_list':chart_data['today_list']}
        render_page = render_to_string("history.html", {'water':water})
        render_page_chart_today = render_to_string("today_chart.html", {'today_list':json.dumps(chart_data['today_list'])})
        render_page_chart_week = render_to_string("week_chart.html", {'week_list':json.dumps(chart_data['week_list']), 'week_avg':int(chart_data['week_avg'])})
        return JsonResponse({'result':result, 'render_history':render_page, 'render_chart_today':render_page_chart_today, 'render_chart_week':render_page_chart_week})