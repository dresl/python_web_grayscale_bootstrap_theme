from django.contrib import admin
from polls.models import Choice, Question, Sidebar
    
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], #'classes': ['collapse']
        	}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date','question_text']
    search_fields = ['question_text']

class SidebarAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title',               {'fields': ['title']}),
        ('Content', {'fields': ['body']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Sidebar, SidebarAdmin)