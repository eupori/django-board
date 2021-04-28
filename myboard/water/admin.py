from django.contrib import admin
from .models import Water, Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'goal', 'total')

@admin.register(Water)
class WaterAdmin(admin.ModelAdmin):
	list_display = ('id', 'time', 'amount')