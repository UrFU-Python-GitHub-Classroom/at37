from django.contrib import admin

from .models import *

class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('title',)
    search_fields = ('title', 'description')

class StatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)
    search_fields = ('id', 'title')

admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Statistic, StatisticAdmin)