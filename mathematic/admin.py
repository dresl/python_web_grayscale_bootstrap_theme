# encoding: utf-8
from django.contrib import admin
from mathematic.models import Brigade, Day

class DayInline(admin.TabularInline):
    model = Day
    extra = 1

class BrigadeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Název brigády',               {'fields': ['brigade_title']}),
        ('Datum publikování', {'fields': ['pub_date'], #'classes': ['collapse']
        	}),
    ]
    inlines = [DayInline]
    list_display = ('brigade_title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date','brigade_title']
    search_fields = ['brigade_title']

admin.site.register(Brigade, BrigadeAdmin)