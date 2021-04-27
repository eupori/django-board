from django.contrib import admin
from .models import Water
# Register your models here.

@admin.register(Water)
class WaterAdmin(admin.ModelAdmin):
	list_display = ('id', 'time', 'amount')