# encoding: utf-8
from django.contrib import admin
from blog.models import Blog, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    list_filter = ('title'),
    search_fields = ('title'),
    list_display = ('title', 'pub_date')
    fieldsets = [
        ('Název',               {'fields': ['title']}),
        ('Zveřejněno', {'fields': ['pub_date']}), #'classes': ['collapse']
        ('Zpráva',               {'fields': ['body']}),
        ('Náhled',            {'fields': ['thumbnail']}),
        ('Likes',            {'fields': ['users_like_it']}),
    ]
    filter_horizontal = ('users_like_it',)
    inlines = [CommentInline]

admin.site.register(Blog, BlogAdmin)